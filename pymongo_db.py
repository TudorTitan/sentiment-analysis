from sentiment_analyis.pymongo_get_database import get_database
#Put all database manipulations here
Vectors = get_database()
articles = Vectors["Assets"]

#Database format: asset, link, date, vector, source, label

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
            'asset': 1,
          'link': 1,
          'date': 1,
          'label': 1,
            'source': 1,
            "score": {"$meta": "vectorSearchScore"} #search score is optional but does not affect speed
        }
      }
    ]
    return articles.aggregate(prep)
