import json
import logging
from itertools import cycle
from math import ceil
from typing import List

from fastapi import APIRouter

from app.api.models import CohortSubmission
from app.utils.clustering.clustering_mvp import batch_cluster


# global variables and services
router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/cluster")
async def cluster_endpoint(sub: dict):
    """ !!! DEPRECATED !!!

    Endpoint takes a list of cohort and submission objects then returns
    clusters based on cohort in groups of 4.

    Arguments:
    ---

    sub (dict): Submission Object Defined by the following form:
    ```
    {
        "1": {
            "1": {
                "Image": "http://lorempixel.com/640/480/abstract",
                "Inappropriate": False,
                "Sensitive": False,
                "Status": "APPROVED",
                "Complexity": 123,
                "Pages": {
                    "1": "http://lorempixel.com/640/480/abstract",
                    "2": "http://lorempixel.com/640/480/abstract",
                },
            },
        },
        "2":{
            "1": {
                "Image": "http://lorempixel.com/640/480/abstract",
                "Inappropriate": False,
                "Sensitive": False,
                "Status": "APPROVED",
                "Complexity": 123,
                "Pages": {
                    "1": "http://lorempixel.com/640/480/abstract",
                    "2": "http://lorempixel.com/640/480/abstract",
                },
            },
        },
    }
    ```

    Returns:
    ---
    `response` json - a list of clusters defined by the following form:
    {
        "1": [["1","2","3","4"]], # CohortID: [Group1[SubmissionIDs],GroupN]
        "2": [["5","6","7","8"]]
    }

    Note:
    ---
    All submissions that are included in this data are post moderation review
    and Approved for COPPA compliance
    """
    response = await batch_cluster(sub)
    return response


@router.post("/cohort-clusters")
async def cohort_clusters(sub: CohortSubmission):
    """Endpoint takes a list of cohort and submission objects then returns
    clusters based on cohort in groups of 4.

    Arguments:
    ---
    sub: CohortSubmission
        sub.submissions: List[dict]
        [
            {
                "id": '1',
                "Image": "http://lorempixel.com/640/480/abstract",
                "Inappropriate": False,
                "Sensitive": False,
                "Status": "APPROVED",
                "Complexity": 123,
            },
            ...
        ]

    Returns: List[List[dict]]
    ---
    list of clusters defined by the following form:
    [
        [
            {'id': '1', 'Complexity': 123},
            {'id': '2', 'Complexity': 124},
            {'id': '3', 'Complexity': 125},
            {'id': '4', 'Complexity': 126},
        ],
        [
            {'id': '5', 'Complexity': 119},
            {'id': '6', 'Complexity': 120},
            {'id': '7', 'Complexity': 121},
            {'id': '8', 'Complexity': 122},
        ],
        ...
    ]
    """
    return await clustering(sub.submissions)


async def clustering(data: List[dict]) -> List[List[dict]]:
    """Splits given list into clusters of 4 based on their complexity.
    """
    num_submissions = len(data)
    remainder = num_submissions % 4
    num_bots = 0 if remainder == 0 else 4 - remainder

    submissions = sorted(
        [{"id": val["id"], "Complexity": val['Complexity']} for val in data],
        key=lambda x: x["Complexity"],
        reverse=True,
    )

    if remainder != 0:
        bots = [
            {"id": f"Bot {bot['id']}", "Complexity": bot['Complexity']}
            for bot in submissions[-num_bots:]
        ]
        i = cycle(range(0, num_submissions - 4, 4))
        for _ in range(num_bots):
            submissions.insert(next(i), bots.pop())

    assert len(submissions) % 4 == 0, "Number of submissions must be a multiple of 4"

    return [submissions[i:i + 4] for i in range(0, len(submissions), 4)]
