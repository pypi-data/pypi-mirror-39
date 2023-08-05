# flake8: noqa
# pylint: disable=trailing-whitespace, pointless-string-statement
"""
@api get /data_mongo/
description: Returns all data_mongo
summary: Fetch all data_mongo
tags:
    - data_mongo
parameters:
    - name: limit
      in: query
      description: The maximum number of data_mongo to fetch
      schema:
        type: integer
    - name: offset
      in: query
      description: The number of data_mongo to offset your query by
      schema:
        type: integer
responses:
    "200":
        description: A list of data_mongo items
    "400":
        description: The request was badly formed or otherwise invalid
    "403":
        description: The auth token was invalid or not provided
"""

"""
@api post /data_mongo/
description: >-
    Submit a new data_mongo item to the service. Do note that not
    all services necessarily support the addition of new items. If it doesn't,
    it shouldn't have this entry but as the documentation is generated,
    the creator may have forgotten this segment.
summary: Add a new  item to the service
tags:
    - data_mongo
responses:
    "201":
        description: Successfully submitted the new data_mongo item
    "400":
        description: The request was badly formed or otherwise invalid
    "403":
        description: The auth token was invalid or not provided
"""

"""
@api get /data_mongo/{id}
description: Fetch a single data_mongo item by ID
summary: Fetch a single data_mongo item by ID
tags:
    - data_mongo
responses:
    "200":
        description: Successfully retrieved item
    "403":
        description: The auth token was invalid or not provided
    "500":
        description: The ID provided is invalid
"""

"""
@api put /data_mongo/{id}
description: Update a data_mongo item in the service
summary: Update a data_mongo item in the service
tags:
    - data_mongo
responses:
    "202":
        description: A success message
    "400":
        description: The request was badly formed or otherwise invalid
    "403":
        description: The auth token was invalid or not provided
    "404":
        description: The item was not found. It was deleted or never existed.
"""

"""
@api delete /data_mongo/{id}
description: Delete a data_mongo item from the service
summary: Delete a data_mongo item from the service
tags:
    - data_mongo
responses:
    "200":
        description: The item was successfully deleted
    "403":
        description: The auth token was invalid or not provided
    "404":
        description: The item was not found. It was deleted or never existed.
"""

"""
@api get /data_mongo/collect/
description: >-
    Performing a GET on the /collect/ endpoint will show any
    currently running collections that have been manually triggered.
    You can see which collector is running and when it was started.
summary: View currently running collections
tags:
    - data_mongo
responses:
    "200":
        description: A JSON object containing the status of active collectors
    "403":
        description: The auth token was invalid or not provided
"""

"""
@api post /data_mongo/collect/
description: >-
    Triggers a manual collection for the data_mongo service. You
    don't need to do this as services will manually run collections at regular
    intervals but it can be useful if you 100% fresh data.
summary: Fetch the latest data_mongo data
tags:
    - data_mongo
responses:
    "202":
        description: A success message stating "Collection received!"
    "403":
        description: The auth token was invalid or not provided
"""

"""
@api post /data_mongo/purge/
description: Purges all data_mongo from the service
summary: Purge all data from the data_mongo service
tags:
    - data_mongo
responses:
    "200":
        description: The purge was successful
    "403":
        description: The auth token was invalid or not provided
"""

"""
@api get /data_mongo/ping/
description: Returns a success code if the service is available
summary: Ping the data_mongo service
tags:
    - data_mongo
responses:
    "200":
        description: The string "pong" indicating the request succeeded
    "403":
        description: The auth token was invalid or not provided
"""


"""
@api get /data_mongo/count/
description: See how many data_mongo are stored in the service
summary: See how many data_mongo are stored in the service
tags:
    - data_mongo
responses:
    "200":
        description: An integer reflecting the total number of data_mongo
    "403":
        description: The auth token was invalid or not provided
"""

"""
@api get /data_mongo/version/
description: Check the current version of the data_mongo service
summary: Check the current version of the data_mongo service
tags:
    - data_mongo
responses:
    "200":
        description: A JSON object showing version and build number
    "403":
        description: The auth token was invalid or not provided
"""
