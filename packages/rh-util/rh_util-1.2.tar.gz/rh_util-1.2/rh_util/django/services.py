class BaseDao:
    __queryset = None
    
    def save(self, objeto):
        objeto.save()
    
    @property
    def queryset(self):
        return self.__queryset
    
    @queryset.setter
    def queryset(self, queryset):
        self.__queryset = queryset
    
    def get_all(self):
        return self.queryset.all()
    
    def get_all_by_fields(self, **fields):
        return self.queryset.filter(**fields)
