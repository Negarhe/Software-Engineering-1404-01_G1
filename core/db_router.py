class TeamPerAppRouter:

    def db_for_read(self, model, **hints):
        return 'team3'

    def db_for_write(self, model, **hints):
        """ALL models write to team3 database"""
        return 'team3'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow all relations since everything is in same database"""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        ALL migrations go to team3 database.
        NO migrations go to default database.
        """
        return db == 'team3'