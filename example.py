"""Short examples of how to use."""

import argparse

import requests
from horde_shared_models.ratings_api import (
    ImageRatingsComparisonTypes,
    RatingsAPIClient,
    SelectableReturnFormats,
    UserValidateRequest,
    UserValidateResponse,
    UserValidateResponseRecord,
)


def main() -> None:
    """Just a proof of concept - but several other pieces of functionality exist."""
    argParser = argparse.ArgumentParser()

    argParser.add_argument("-k", "--key", required=True, help="Your horde API key.")
    argParser.add_argument("-f", "--file", required=True, help="The file to write the response to.")
    argParser.add_argument("-u", "--user_id", required=True, help="The user_id (number only) to test against.")
    args = argParser.parse_args()

    # apiKey = os.environ.get("HORDE_API_KEY")

    # class args:
    #     key = CHANGE_ME
    #     user_id = "6572"
    #     file = "out.json"

    ratingsAPIClient = RatingsAPIClient()
    userValidateRequest = UserValidateRequest(
        apikey=args.key,
        user_id=args.user_id,
        format=SelectableReturnFormats.json,
        rating=8,
        rating_comparison=ImageRatingsComparisonTypes.greater_than_equal,
        min_ratings=0,
    )

    response: requests.Response = ratingsAPIClient.submitRequest(userValidateRequest)
    responseJson = response.json()
    print(responseJson)
    validate_response = UserValidateResponse(**responseJson)

    print(f"{validate_response.total=}")
    first_rating: UserValidateResponseRecord = validate_response.ratings[0]

    print(f"{first_rating.image=}")
    print(f"{first_rating.rating=}")
    print(f"{first_rating.artifacts=}")
    print(f"{first_rating.average=}")
    print(f"{first_rating.times_rated=}")

    with open(args.file, "w") as fileOutHandle:
        fileOutHandle.write(first_rating.json())


if __name__ == "__main__":
    main()
