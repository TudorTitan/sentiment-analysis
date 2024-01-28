from sentiment_analyis.pymongo_get_database import get_database
#Put all database manipulations here
Vectors = get_database()
articles = Vectors["table"]

#Database format: link, date, vector, class

#Vector search for vec; knn with k = limit, and candidates/limit typically 20
def query(vec,limit,candidates):
    prep = [
      {
        '$vectorSearch': {
          'index': 'vector_index',
          'path': 'vector',
          'queryVector': vec,
          'numCandidates': candidates,
          'limit': limit
        }
      }, {
        '$project': {
          '_id': 0,
          'link': 1,
          'date': 1,
          'class': 1,
            "score": {"$meta": "vectorSearchScore"} #search score is optional but does not affect speed
        }
      }
    ]
    return articles.aggregate(prep)
