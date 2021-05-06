from copy import copy


class FakeDb():
    """
    Toy model of database. Not real database just python object behaving like object
    communicating with a database.
    """
    def __init__(self):
        self.tables = {}
        # The insertion count is used as an automatically generated ID. Hence need to
        # store map keeping track how many insertions were made to each table
        self.insertions = {}

    def add(self, row):
        model = type(row)
        if model not in self.tables:
            # Tables are implemented as dicts with model's primary_key used is dict's key
            # Very basic and inefficient of course, but this is just a toy model of db
            self.tables[model] = {}
        try:
            primary_key = row.primary_key
        except AttributeError:
            # Each table needs primary_key to be used as unique identifier
            raise TypeError("Valid database mode has to have attribute \"primary_key\"")

        try:
            pk_value = getattr(row, primary_key)
        except AttributeError:
            setattr(row, primary_key, self._generate_id(type(row)))
            pk_value = getattr(row, primary_key)

        if pk_value in self.tables:
            raise ValueError("Duplicate primary keys detected")

        # Here we want to model a functionality of database. If we assigned
        # row to table dict, then by directly manipulating row object, we would be
        # manipulating database. We don't want that. Database is manipulated by
        # calling update, not by direct modification
        self.tables[model][pk_value] = row.copy()

        insertions = self.insertions.get(model, 0)
        self.insertions[model] = insertions+1

    def update(self, row_update, pk_value):
        model = type(row_update)
        old_row = self.get(model, pk_value)
        if old_row:
            update_dict = {attr: val for attr, val in row_update.__dict__.items() if val}
            for attr, val in update_dict.items():
                setattr(old_row, attr, val)
            self.delete(model, pk_value)
            self.add(old_row)

            # We actually didn't do new insertion, decrement counter then
            insertions = self.insertions.get(model, 0)
            self.insertions[model] = insertions-1

    def get(self, model, pk_value):
        table = self._get_table(model)

        res = table.get(pk_value, None)
        # Again, we need to copy the result. Otherwise modifying the returned object
        # would modify the database without actually calling update
        # None cannot be copied. Of course we don't need the res is not None explicitely
        # but without it this line is quite difficult to understand
        return res.copy() if res is not None else res

    def get_all(self, model):
        table = self._get_table(model)
        return [row.copy() for row in table.values()]

    def delete(self, model, pk_value):
        table = self._get_table(model)

        return table.pop(pk_value, None)

    def _generate_id(self, model):
        return self.insertions.get(model, 0)+1

    def _get_table(self, model):
        try:
            table = self.tables[model]
        except KeyError:
            raise KeyError(f"No table with model {model}")
        return table


class DbModel():
    """
    This is a base model that should be inheritted by all models
    used to create database table
    """
    def __eq__(self, other):
        """
        Since model is just a row entry, two models with identical
        attributes should be equal.

        This is especially important because we are inserting copies
        of model into our fake database, hence
        not implementing this function in this way would cause the
        object used to insert into the database to NOT be equal to the
        object in the database.
        """
        if (isinstance(other, DbModel)):
            return self.__dict__ == other.__dict__

    def copy(self):
        """This funciton is not necessary of course - we could just directly call copy(model_obj)
        when we need a copy of DbModel. But this way we ensure that FakeDb is dealing with proper
        Model object (ones that inherits this DbModel)"""
        return copy(self)


def session_connect():
    return FakeDb()
