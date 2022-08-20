# Author: Craig O'Loughlin
# Date: 7/31/2022
# Version: 1.0 (Project 1)
# SNHU CS340 Module Five Project 1

from pymongo import MongoClient, cursor
from pymongo.results import *
from pymongo.errors import *
from bson.objectid import ObjectId

class MongoCRUD(object):

    """ Helper class for connecting to and performing CRUD operations on a mongoDB server """

    def __init__(self, target='admin.system.users', username=None, password=None):

        """Start a connection to mongod with authorization and target the specified database / collection.

        Currently establishes connection on localhost:27017 only.
        Currently only works with a single database/collection.

        Keyword arguments:

        target -- the database and collection to use. Dot notation such as "AAC.animals" should be used.
        username -- Authentification username for the database.
        password -- Authentification password for the database user.
        """

        # expecting format DB.COLLECTION ex "AAC.animals"
        targets = target.split('.')
        self._targetDB = targets[0]
        self._targetColl = '.'.join(targets[1:])

        # background connection process returns immediately without verifying connection successful
        print("Attempting connection to MongoDB server @ localhost:27017..")
        self._client = MongoClient('mongodb://%s:%s@localhost:27017' % (username, password), 
                                    authSource=self._targetDB, serverSelectionTimeoutMS=2500)
            
        # check connection using ping command
        try:
            self._client.admin.command('ping')
            print('Connection successful!')
            self._DBconnected = True
            self._database = self._client[self._targetDB]
            self._collection = self._database[self._targetColl]

        # report connection errors/auth errors
        except PyMongoError as error:
            print(f'On CONNECT: {error}')
            self._DBconnected = False

    def _verifyConnection(self):
        '''Disallow CRUD operations without valid connection'''
        if not self._DBconnected:
            raise ConnectionFailure('Cannot perform CRUD operation without an active connection to MongoDB server.')

    def _verifyInsert(self, insertID):
        '''Check that an inserted document exists in db'''
        if self._collection.find_one(insertID) is None:
            raise WriteError(f'Document was not successfully verified in database ({insertID} not found).')
        print(f'Data inserted successfully with ObjectID {insertID}')

    def _buildSearchTerm(self, query):
        '''Builds a document filter from one or multiple queries. Multiple queries are OR'd'''
        return query[0] if len(query) <= 1 else {'$or': [q for q in query]}

    def _buildUpdateTerm(self, updateInfo):
        '''Builds an update term by adding the default $set operator to any update request'''
        return {'$set': updateInfo}

    def _checkEmptyFilter(self, filter):
        '''Warning thrown against sending any empty filter'''
        for value in filter:
            if value == {}:
                raise InvalidOperation(f'WARNING: The chosen filter {filter} may delete ALL entries.\n'
                                      + 'If you would like to do this, set safetyOn=False in argument.\n'
                                      + 'No action was performed.')


    def create(self, data) -> bool:

        '''Insert a new document into the target collection
        
        Keyword arguments:

        data -- Dictionary object representing JSON document for insertion. Key values must be strings

        Returns:
        True upon successful insertion else False.
        '''

        #check empty condition
        if len(data) == 0:
            print("Nothing to save, because data parameter is empty.")
            return False
                
        # attempt insert if connection is available
        try:
            self._verifyConnection()
            print(f'Performing insert: {data}')
            insertID =  self._collection.insert_one(data).inserted_id # to pymongo
            self._verifyInsert(insertID)
            return True

        # report any mongoDB errors from insert
        except PyMongoError as error:
            print(f'On CREATE: {error}')
            return False


    def read(self, *query) -> cursor:

        '''Query the target database for a document matching the input parameters. Multiple parameters entered as additional
        arguments will be OR'd (results given for matches to any of the arguments).
        
        Keyword arguments:

        query -- One or many dictionary arguments representing the key/values to query from database.
                examples:

                    {'name': 'Bob', 'age': 45}
                    returns documents with 45 year old Bobs.

                    {'name': 'Bob'}, {'age': 45}
                    returns documents with any Bob OR anyone 45 years old.

        Returns:

        PyMongo cursor, an object to iterate document results if any,
        or None upon error.
        '''

        # query database if connection available, any results (including no results) returned in cursor
        try: 
            self._verifyConnection()
            search = self._buildSearchTerm(query)
            print(f'Performing query: {search}') 
            return self._collection.find(search)  # to pymongo      

        # report any mongoDB errors from query
        except PyMongoError as error:
            print(f'On READ: {error}')
            return None  

    def update(self, filter, updateInfo) -> UpdateResult:

        '''Find a target set of documents that match the given filter, and then update document parameters per the given update info.
        This operation performs an update ($set) instead of complete replacement of document. A single filter argument is excepted.
        
        Keyword arguments:

        filter -- A single filter expression. Documents matching the filter criteria will be targetted for update.

        updateInfo -- A single dictionary argument contain field:value pairs to update in the target documents.

        Returns:

        An instance of PyMongo UpdateResult containing document count and JSON result, or None on failure.
        
        '''

        # check that the update field is not empty
        if len(updateInfo) == 0:
            print("Nothing to update, because update parameter is empty.")
            return None
        
        # build and send request to server if connection available, result object returned
        try:
            self._verifyConnection()
            update = self._buildUpdateTerm(updateInfo)
            print(f'Performing update: {update} \nwith filter: {filter}')
            result = self._collection.update_many(filter, update) # to pymongo
            print(f'{result.modified_count} document(s) updated.\n{result.raw_result}')
            return result

        # report any mongoDB errors from update command
        except PyMongoError as error:
            print(f'On UPDATE: {error}')
            return None

    def delete(self, *filter, safetyOn=True) -> DeleteResult:

        '''Delete one or many documents from the target collection matching the filter parameters
        
        Keyword arguments:

        *filter - One or many dictionary arguments representing the fields to search for. Multiple arguments ar OR'd.
                examples:

                    {'name': 'Bob', 'age': 45}
                    deletes all 45 year old Bobs.

                    {'name': 'Bob'}, {'age': 45}
                    deletes all Bobs along with all 45 year olds.

        safetyOn - Set to False to allow the universal field {} as a filter which will delete all entries in the collection.

        Returns:

        An instance of PyMongo DeleteResult containing document count and JSON result, or None on failure.
        '''

        # build and send delete request to server if connection available, result object returned
        try:
            self._verifyConnection()
            search = self._buildSearchTerm(filter)
            if safetyOn: # check for all documents filter {}
                self._checkEmptyFilter(filter) # throws a pymongo error if {} is found
            print(f'Performing delete: {search}')
            result = self._collection.delete_many(search) # to pymongo
            print(f'{result.deleted_count} document(s) deleted.\n{result.raw_result}')
            return result

        # report any mongoDB errors from delete command
        except PyMongoError as error:
            print(f'On DELETE: {error}')
            return None

    



