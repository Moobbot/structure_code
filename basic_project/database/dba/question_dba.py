# database/database_access/question_dba.py
import os
import sys

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

from configs import db_config
from utils.util import (
    normalize_id,
    prepare_bulk_updates,
    validate_condition,
)
from utils.json_encoder import convert_objectid_to_str

from database.dbo.question_dbo import QuestionDBO
from database.dba.dba import DBA

from bson import ObjectId
from typing import Any, Dict, List
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure, PyMongoError


class QuestionDBA(DBA):
    def __init__(self, connection):
        super().__init__(db_config.SCHEMA["QUESTIONS"])
        self.dba = DBA.create_dba(
            db_config.DB_TYPE, connection, [db_config.CONNECT["QUESTION_COLLECTION"]]
        )

    def transaction(self, query_func, **kwargs):
        """Perform a transaction. Implementation depends on specific use case."""
        if self.client is None:
            self.logger.log_error("No MongoDB client available for transaction")
            return None

        with self.client.start_session() as session:
            try:
                session.start_transaction()
                result = query_func(session=session, **kwargs)
                session.commit_transaction()
                self.client.logger.log_info("Transaction committed successfully")
            except (
                ConnectionFailure,
                ServerSelectionTimeoutError,
                PyMongoError,
            ) as err:
                self.client.logger.log_error("Transaction failed", err)
                session.abort_transaction()
                self.client.logger.log_info("Transaction aborted")
                return None
        return result

    def find_by_id(self, id: ObjectId, session=None) -> QuestionDBO:
        try:
            normalized_id = normalize_id(id)
            result = self.collection.find_one({"_id": normalized_id}, session=session)
            if result:
                return QuestionDBO(**result)
            return None
        except ValueError as e:
            print(e)
            return None

    def find_one(self, condition: Dict[str, Any], session=None) -> QuestionDBO:
        try:
            validated_condition = validate_condition(condition)
            result = self.collection.find_one(validated_condition, session=session)
            if result:
                return QuestionDBO(**result)
            return None
        except ValueError as e:
            print(e)
            return None

    def find_many(
        self, n: int, condition: Dict[str, Any], session=None
    ) -> List[QuestionDBO]:
        try:
            validated_condition = validate_condition(condition)
            cursor = self.collection.find(validated_condition, session=session).limit(n)
            return [QuestionDBO(**data) for data in cursor]
        except ValueError as e:
            print(e)
            return None

    def update_one_by_id(
        self, id: ObjectId, new_value: Dict[str, Any], session=None
    ) -> bool:
        try:
            normalized_id = normalize_id(id)
            result = self.collection.update_one(
                {"_id": normalized_id}, {"$set": new_value}, session=session
            )
            return result.modified_count > 0
        except ValueError as e:
            print(e)
            return False

    def update_many_by_id(
        self, ids: List[ObjectId], new_values: List[Dict[str, Any]], session=None
    ) -> bool:
        try:
            bulk_updates = prepare_bulk_updates(ids, new_values)
            result = self.collection.bulk_write(bulk_updates, session=session)
            return result.modified_count > 0
        except ValueError as e:
            print(e)
            return False

    def insert(self, obj: QuestionDBO, session=None) -> ObjectId:
        try:
            data = obj.to_json()
            result = self.collection.insert_one(data, session=session)
            return result.inserted_id
        except ValueError as e:
            print(e)
            return None

    def delete_by_id(self, id: ObjectId, session=None) -> bool:
        try:
            normalized_id = normalize_id(id)
            result = self.collection.delete_one({"_id": normalized_id}, session=session)
            return result.deleted_count > 0
        except ValueError as e:
            print(e)
            return False

    def get_questions(self, N, session=None):
        questions = self.find_many(N, {}, session=session)
        if questions is None:
            return []
        questions_serializable = [
            convert_objectid_to_str(question) for question in questions
        ]
        return questions_serializable
    def join_collections(self, collection_names):
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": collection_names[1],
                        "localField": "questions._id",
                        "foreignField": "_id",
                        "as": "questions_detail",
                    }
                },
                {"$unwind": "$questions_detail"},
                {
                    "$replaceRoot": {
                        "newRoot": {"$mergeObjects": ["$$ROOT", "$questions_detail"]}
                    }
                },
            ]

            local_collection_name = collection_names[0]
            joined_data = list(
                self.collections[local_collection_name].aggregate(pipeline)
            )

            # Use a temporary collection to store the joined data
            self.collection = self.connection.database["joined_collection"]
            self.collection.drop()  # Clear the collection if it exists
            if joined_data:
                self.collection.insert_many(joined_data)
            return self.collection
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    # Example usage
    question_dba = QuestionDBA()
    data = question_dba.transaction(question_dba.get_questions, N=5)
    print(data)

    # Insert a new question
    # new_question = Question(
    #     id=ObjectId(),
    #     category=1,
    #     subcategory="Math",
    #     content="What is 2+2?",
    #     answers=["2", "3", "4", "5"],
    #     correct_answer="4",
    #     multimedia=ObjectId(),
    # )

    # inserted_id = question_dba.insert(new_question)
    # print(f"Inserted question with ID: {inserted_id}")

    # # Find a question by ID
    # question = question_dba.find_by_id(inserted_id)
    # print(question)

    # # Update a question by ID
    # update_result = question_dba.update_one_by_id(
    #     inserted_id, {"content": "What is 3+3?"}
    # )
    # print(f"Update successful: {update_result}")

    # # Find many questions
    # questions = question_dba.find_many(5, {"category": 1})
    # for q in questions:
    #     print(q)

    # # Delete a question by ID
    # delete_result = question_dba.delete_by_id(inserted_id)
    # print(f"Delete successful: {delete_result}")
