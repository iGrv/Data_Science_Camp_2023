import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse


# Create the API
api = FastAPI()

# Define a list with initial records
RECORDS = [
    "First record",
    "Second record",
    "Third record",
    "Fourth record",
    "Fifth record",
    "Sixth record",
    "Seventh record",
    "Eighth record",
    "Ninth record",
    "Tenth record",
    "Eleventh record",
    "Twelfth record"
]


@api.get("/api/last_10_records")
async def get_records() -> JSONResponse:
    """
    Returns last 10 records.

    Returns:
        JSONResponse: List containing last 10 records
    """
    return JSONResponse(content={"last 10 added records": RECORDS[-10:]})


@api.post("/api/add_record/{record}")
async def add_record(record: str) -> PlainTextResponse:
    """
    Adds the specified record.

    Args:
        record (str): Record to add

    Returns:
        PlainTextResponse: Message that a new record was added
    """
    RECORDS.append(record)
    return PlainTextResponse(content=f"New added record: {record}")


@api.delete("/api/delete_record/{record}")
async def delete_record(record: str) -> PlainTextResponse:
    """
    Removes the specified record if it is found.

    Args:
        record (str): Record to remove

    Returns:
        PlainTextResponse: Message that the record was removed or message that the record was not found
    """
    try:
        RECORDS.remove(record)
    except ValueError:
        return PlainTextResponse(status_code=404, content=f"Record not found")
    else:
        return PlainTextResponse(content=f"Removed record: {record}")


if __name__ == "__main__":

    # Run API on the web server on localhost on port 8080
    uvicorn.run("main:api", port=8080)
