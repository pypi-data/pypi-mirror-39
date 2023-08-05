import itertools
import math

from flask import current_app
from flask import url_for
from sqlalchemy import exc as sa_exc, inspect
from sqlalchemy import util, log
from sqlalchemy.orm import properties
from sqlalchemy.orm import (
    util as orm_util
)
from sqlalchemy.orm.strategies import AbstractRelationshipLoader


class Page(object):
    
    def __init__(self, items, page, page_size, total):
        self.items = items
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))


def paginate(query, page, page_size):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    total = query.order_by(None).count()
    return Page(items, page, page_size, total)


class Pagination:
    def __init__(self, request, query, blue_print, nome_da_view, key_name, schema):
        self.request = request
        self.query = query
        self.resource_for_url = blue_print + '.' + nome_da_view.__name__
        self.key_name = key_name
        self.schema = schema
        self.results_per_page = current_app.config['PAGINATION_PAGE_SIZE']
        self.page_argument_name = current_app.config['PAGINATION_PAGE_ARGUMENT_NAME']
    
    def paginate_query(self):
        page_number = self.request.args.get(self.page_argument_name, 1, type=int)
        
        paginated_objects = paginate(self.query, page_number, self.results_per_page)
        objects = paginated_objects.items
        if paginated_objects.has_previous:
            previous_page_url = url_for(
                self.resource_for_url,
                page=page_number - 1,
                _external=True)
        else:
            previous_page_url = None
        if paginated_objects.has_next:
            next_page_url = url_for(
                self.resource_for_url,
                page=page_number + 1,
                _external=True)
        else:
            next_page_url = None
        dumped_objects = self.schema.dump(objects, many=True).data
        return ({
            self.key_name: dumped_objects,
            'previous': previous_page_url,
            'next': next_page_url,
            'count': paginated_objects.total
        })


def create_object_from_sql_alchemy_row(row, instance):
    """ Monta objeto a partir de uma linha de query do SQL Alchemy"""
    fields = {field.key: atrr for atrr, field in instance.__mapper__.columns.items()}
    for column in row.keys():
        if column in fields:
            setattr(instance, fields[column], row[column])
    return instance


@log.class_logger
@properties.RelationshipProperty.strategy_for(lazy="subquery_with_nolock")
class SubqueryLoaderWithNoLock(AbstractRelationshipLoader):
    __slots__ = 'join_depth',
    
    def __init__(self, parent, strategy_key):
        super(SubqueryLoaderWithNoLock, self).__init__(parent, strategy_key)
        self.join_depth = self.parent_property.join_depth
    
    def init_class_attribute(self, mapper):
        self.parent_property._get_strategy((("lazy", "select"),)).init_class_attribute(mapper)
    
    def setup_query(
            self, context, entity,
            path, loadopt, adapter,
            column_collection=None,
            parentmapper=None, **kwargs):
        
        if not context.query._enable_eagerloads:
            return
        elif context.query._yield_per:
            context.query._no_yield_per("subquery")
        
        path = path[self.parent_property]
        
        # build up a path indicating the path from the leftmost
        # entity to the thing we're subquery loading.
        with_poly_info = path.get(
            context.attributes,
            "path_with_polymorphic", None)
        if with_poly_info is not None:
            effective_entity = with_poly_info.entity
        else:
            effective_entity = self.mapper
        
        subq_path = context.attributes.get(
            ('subquery_path', None),
            orm_util.PathRegistry.root)
        
        subq_path = subq_path + path
        
        # if not via query option, check for
        # a cycle
        if not path.contains(context.attributes, "loader"):
            if self.join_depth:
                if path.length / 2 > self.join_depth:
                    return
            elif subq_path.contains_mapper(self.mapper):
                return
        
        leftmost_mapper, leftmost_attr, leftmost_relationship = \
            self._get_leftmost(subq_path)
        
        orig_query = context.attributes.get(
            ("orig_query", SubqueryLoaderWithNoLock),
            context.query)
        
        # generate a new Query from the original, then
        # produce a subquery from it.
        left_alias = self._generate_from_original_query(
            orig_query, leftmost_mapper,
            leftmost_attr, leftmost_relationship,
            entity.entity_zero
        )
        
        # generate another Query that will join the
        # left alias to the target relationships.
        # basically doing a longhand
        # "from_self()".  (from_self() itself not quite industrial
        # strength enough for all contingencies...but very close)
        q = orig_query.session.query(effective_entity).with_hint(effective_entity, 'WITH (NOLOCK)')
        q._attributes = {
            ("orig_query", SubqueryLoaderWithNoLock): orig_query,
            ('subquery_path', None): subq_path
        }
        
        q = q._set_enable_single_crit(False)
        to_join, local_attr, parent_alias = \
            self._prep_for_joins(left_alias, subq_path)
        q = q.order_by(*local_attr)
        q = q.add_columns(*local_attr)
        q = self._apply_joins(
            q, to_join, left_alias,
            parent_alias, effective_entity)
        
        q = self._setup_options(q, subq_path, orig_query, effective_entity)
        q = self._setup_outermost_orderby(q)
        
        # add new query to attributes to be picked up
        # by create_row_processor
        path.set(context.attributes, "subquery", q)
    
    def _get_leftmost(self, subq_path):
        subq_path = subq_path.path
        subq_mapper = orm_util._class_to_mapper(subq_path[0])
        
        # determine attributes of the leftmost mapper
        if self.parent.isa(subq_mapper) and \
                self.parent_property is subq_path[1]:
            leftmost_mapper, leftmost_prop = \
                self.parent, self.parent_property
        else:
            leftmost_mapper, leftmost_prop = \
                subq_mapper, \
                subq_path[1]
        
        leftmost_cols = leftmost_prop.local_columns
        
        leftmost_attr = [
            getattr(
                subq_path[0].entity,
                leftmost_mapper._columntoproperty[c].key)
            for c in leftmost_cols
        ]
        
        return leftmost_mapper, leftmost_attr, leftmost_prop
    
    def _generate_from_original_query(
            self,
            orig_query, leftmost_mapper,
            leftmost_attr, leftmost_relationship, orig_entity
    ):
        # reformat the original query
        # to look only for significant columns
        q = orig_query._clone().correlate(None)
        
        # set a real "from" if not present, as this is more
        # accurate than just going off of the column expression
        if not q._from_obj and orig_entity.mapper.isa(leftmost_mapper):
            q._set_select_from([orig_entity], False)
        target_cols = q._adapt_col_list(leftmost_attr)
        
        # select from the identity columns of the outer
        q._set_entities(target_cols)
        
        distinct_target_key = leftmost_relationship.distinct_target_key
        
        if distinct_target_key is True:
            q._distinct = True
        elif distinct_target_key is None:
            # if target_cols refer to a non-primary key or only
            # part of a composite primary key, set the q as distinct
            for t in set(c.table for c in target_cols):
                if not set(target_cols).issuperset(t.primary_key):
                    q._distinct = True
                    break
        
        if q._order_by is False:
            q._order_by = leftmost_mapper.order_by
        
        # don't need ORDER BY if no limit/offset
        if q._limit is None and q._offset is None:
            q._order_by = None
        
        # the original query now becomes a subquery
        # which we'll join onto.
        
        embed_q = q.with_labels().subquery()
        left_alias = orm_util.AliasedClass(
            leftmost_mapper, embed_q,
            use_mapper_path=True)
        return left_alias
    
    def _prep_for_joins(self, left_alias, subq_path):
        # figure out what's being joined.  a.k.a. the fun part
        to_join = []
        pairs = list(subq_path.pairs())
        
        for i, (mapper, prop) in enumerate(pairs):
            if i > 0:
                # look at the previous mapper in the chain -
                # if it is as or more specific than this prop's
                # mapper, use that instead.
                # note we have an assumption here that
                # the non-first element is always going to be a mapper,
                # not an AliasedClass
                
                prev_mapper = pairs[i - 1][1].mapper
                to_append = prev_mapper if prev_mapper.isa(mapper) else mapper
            else:
                to_append = mapper
            
            to_join.append((to_append, prop.key))
        
        # determine the immediate parent class we are joining from,
        # which needs to be aliased.
        
        if len(to_join) < 2:
            # in the case of a one level eager load, this is the
            # leftmost "left_alias".
            parent_alias = left_alias
        else:
            info = inspect(to_join[-1][0])
            if info.is_aliased_class:
                parent_alias = info.entity
            else:
                # alias a plain mapper as we may be
                # joining multiple times
                parent_alias = orm_util.AliasedClass(
                    info.entity,
                    use_mapper_path=True)
        
        local_cols = self.parent_property.local_columns
        
        local_attr = [
            getattr(parent_alias, self.parent._columntoproperty[c].key)
            for c in local_cols
        ]
        return to_join, local_attr, parent_alias
    
    def _apply_joins(
            self, q, to_join, left_alias, parent_alias,
            effective_entity):
        
        ltj = len(to_join)
        if ltj == 1:
            to_join = [
                getattr(left_alias, to_join[0][1]).of_type(effective_entity)
            ]
        elif ltj == 2:
            to_join = [
                getattr(left_alias, to_join[0][1]).of_type(parent_alias),
                getattr(parent_alias, to_join[-1][1]).of_type(effective_entity)
            ]
        elif ltj > 2:
            middle = [
                (
                    orm_util.AliasedClass(item[0])
                    if not inspect(item[0]).is_aliased_class
                    else item[0].entity,
                    item[1]
                ) for item in to_join[1:-1]
            ]
            inner = []
            
            while middle:
                item = middle.pop(0)
                attr = getattr(item[0], item[1])
                if middle:
                    attr = attr.of_type(middle[0][0])
                else:
                    attr = attr.of_type(parent_alias)
                
                inner.append(attr)
            
            to_join = [
                          getattr(left_alias, to_join[0][1]).of_type(inner[0].parent)
                      ] + inner + [
                          getattr(parent_alias, to_join[-1][1]).of_type(effective_entity)
                      ]
        
        for attr in to_join:
            q = q.join(attr, from_joinpoint=True)
        return q
    
    def _setup_options(self, q, subq_path, orig_query, effective_entity):
        # propagate loader options etc. to the new query.
        # these will fire relative to subq_path.
        q = q._with_current_path(subq_path)
        q = q._conditional_options(*orig_query._with_options)
        if orig_query._populate_existing:
            q._populate_existing = orig_query._populate_existing
        
        return q
    
    def _setup_outermost_orderby(self, q):
        if self.parent_property.order_by:
            # if there's an ORDER BY, alias it the same
            # way joinedloader does, but we have to pull out
            # the "eagerjoin" from the query.
            # this really only picks up the "secondary" table
            # right now.
            eagerjoin = q._from_obj[0]
            eager_order_by = \
                eagerjoin._target_adapter. \
                    copy_and_process(
                    util.to_list(
                        self.parent_property.order_by
                    )
                )
            q = q.order_by(*eager_order_by)
        return q
    
    class _SubqCollections(object):
        """Given a :class:`.Query` used to emit the "subquery load",
        provide a load interface that executes the query at the
        first moment a value is needed.

        """
        _data = None
        
        def __init__(self, subq):
            self.subq = subq
        
        def get(self, key, default):
            if self._data is None:
                self._load()
            return self._data.get(key, default)
        
        def _load(self):
            self._data = dict(
                (k, [vv[0] for vv in v])
                for k, v in itertools.groupby(
                    self.subq,
                    lambda x: x[1:]
                )
            )
        
        def loader(self, state, dict_, row):
            if self._data is None:
                self._load()
    
    def create_row_processor(
            self, context, path, loadopt,
            mapper, result, adapter, populators):
        if not self.parent.class_manager[self.key].impl.supports_population:
            raise sa_exc.InvalidRequestError(
                "'%s' does not support object "
                "population - eager loading cannot be applied." %
                self)
        
        path = path[self.parent_property]
        
        subq = path.get(context.attributes, 'subquery')
        
        if subq is None:
            return
        
        assert subq.session is context.session, (
            "Subquery session doesn't refer to that of "
            "our context.  Are there broken context caching "
            "schemes being used?"
        )
        
        local_cols = self.parent_property.local_columns
        
        # cache the loaded collections in the context
        # so that inheriting mappers don't re-load when they
        # call upon create_row_processor again
        collections = path.get(context.attributes, "collections")
        if collections is None:
            collections = self._SubqCollections(subq)
            path.set(context.attributes, 'collections', collections)
        
        if adapter:
            local_cols = [adapter.columns[c] for c in local_cols]
        
        if self.uselist:
            self._create_collection_loader(
                context, collections, local_cols, populators)
        else:
            self._create_scalar_loader(
                context, collections, local_cols, populators)
    
    def _create_collection_loader(
            self, context, collections, local_cols, populators):
        def load_collection_from_subq(state, dict_, row):
            collection = collections.get(
                tuple([row[col] for col in local_cols]),
                ()
            )
            state.get_impl(self.key). \
                set_committed_value(state, dict_, collection)
        
        populators["new"].append((self.key, load_collection_from_subq))
        if context.invoke_all_eagers:
            populators["eager"].append((self.key, collections.loader))
    
    def _create_scalar_loader(
            self, context, collections, local_cols, populators):
        def load_scalar_from_subq(state, dict_, row):
            collection = collections.get(
                tuple([row[col] for col in local_cols]),
                (None,)
            )
            if len(collection) > 1:
                util.warn(
                    "Multiple rows returned with "
                    "uselist=False for eagerly-loaded attribute '%s' "
                    % self)
            
            scalar = collection[0]
            state.get_impl(self.key). \
                set_committed_value(state, dict_, scalar)
        
        populators["new"].append((self.key, load_scalar_from_subq))
        if context.invoke_all_eagers:
            populators["eager"].append((self.key, collections.loader))