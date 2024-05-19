"""Util that calls Imdb Search API.

In order to set this up, follow instructions at:
"""
import json
from typing import Dict, List, Optional

import aiohttp
import requests
from langchain_core.pydantic_v1 import BaseModel, Extra, SecretStr, root_validator
from langchain_core.utils import get_from_dict_or_env

from ImdbAPI import ImdbAPI
imdbAPI = ImdbAPI()

#Genres divided by coma ','
genres = "action,drama"
IMDB_API_URL = f"https://www.imdb.com/search/title/?genres={genres}e&sort=num_votes,desc"


class ImdbSearchAPIWrapper(BaseModel):
    """Wrapper for Imdb Search API."""

    #imdb_api_key: SecretStr

    class Config:
        """Configuration for this pydantic object."""
        #extra = Extra.forbid

    # @root_validator(pre=True)
    # def validate_environment(cls, values: Dict) -> Dict:
    #     """Validate that api key and endpoint exists in environment."""
    #     imdb_api_key = get_from_dict_or_env(
    #         values, "imdb_api_key", "IMDB_API_KEY"
    #     )
    #     values["imdb_api_key"] = imdb_api_key

    #     return values

    def raw_results(
        self,
        query: str,
        max_results: Optional[int] = 5,
        search_depth: Optional[str] = "advanced",
        include_domains: Optional[List[str]] = [],
        exclude_domains: Optional[List[str]] = [],
        include_answer: Optional[bool] = False,
        include_raw_content: Optional[bool] = False,
        include_images: Optional[bool] = False,
    ) -> Dict:
        params = {
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "include_images": include_images,
        }
        return json(imdbAPI.search(query))

    def results(
        self,
        query: str,
        max_results: Optional[int] = 5,
        search_depth: Optional[str] = "advanced",
        include_domains: Optional[List[str]] = [],
        exclude_domains: Optional[List[str]] = [],
        include_answer: Optional[bool] = False,
        include_raw_content: Optional[bool] = False,
        include_images: Optional[bool] = False,
    ) -> List[Dict]:
        """Run query through Imdb Search and return metadata.

        Args:
            query: The query to search for.
            max_results: The maximum number of results to return.
            search_depth: The depth of the search. Can be "basic" or "advanced".
            include_domains: A list of domains to include in the search.
            exclude_domains: A list of domains to exclude from the search.
            include_answer: Whether to include the answer in the results.
            include_raw_content: Whether to include the raw content in the results.
            include_images: Whether to include images in the results.
        Returns:
            query: The query that was searched for.
            follow_up_questions: A list of follow up questions.
            response_time: The response time of the query.
            answer: The answer to the query.
            images: A list of images.
            results: A list of dictionaries containing the results:
                title: The title of the result.
                url: The url of the result.
                content: The content of the result.
                score: The score of the result.
                raw_content: The raw content of the result.
        """  # noqa: E501
        
        #
        # raw_search_results = self.raw_results(
        #     query,
        #     max_results=max_results,
        #     search_depth=search_depth,
        #     include_domains=include_domains,
        #     exclude_domains=exclude_domains,
        #     include_answer=include_answer,
        #     include_raw_content=include_raw_content,
        #     include_images=include_images,
        # )
        # return self.clean_results(raw_search_results["results"])
        
        return imdbAPI.search(query)


    async def raw_results_async(
        self,
        query: str,
        max_results: Optional[int] = 5,
        search_depth: Optional[str] = "advanced",
        include_domains: Optional[List[str]] = [],
        exclude_domains: Optional[List[str]] = [],
        include_answer: Optional[bool] = False,
        include_raw_content: Optional[bool] = False,
        include_images: Optional[bool] = False,
    ) -> Dict:
        """Get results from the Imdb Search API asynchronously."""

        # Function to perform the API call
        async def fetch() -> str:
            params = {
                "api_key": self.imdb_api_key.get_secret_value(),
                "query": query,
                "max_results": max_results,
                "search_depth": search_depth,
                "include_domains": include_domains,
                "exclude_domains": exclude_domains,
                "include_answer": include_answer,
                "include_raw_content": include_raw_content,
                "include_images": include_images,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(f"not implemented", json=params) as res:
                    if res.status == 200:
                        data = await res.text()
                        return data
                    else:
                        raise Exception(f"Error {res.status}: {res.reason}")

        results_json_str = await fetch()
        return json.loads(results_json_str)

    async def results_async(
        self,
        query: str,
        max_results: Optional[int] = 5,
        search_depth: Optional[str] = "advanced",
        include_domains: Optional[List[str]] = [],
        exclude_domains: Optional[List[str]] = [],
        include_answer: Optional[bool] = False,
        include_raw_content: Optional[bool] = False,
        include_images: Optional[bool] = False,
    ) -> List[Dict]:
        results_json = await self.raw_results_async(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_answer=include_answer,
            include_raw_content=include_raw_content,
            include_images=include_images,
        )
        return self.clean_results(results_json["results"])

    def clean_results(self, results: List[Dict]) -> List[Dict]:
        """Clean results from IMDB Search API."""
        clean_results = []
        for result in results:
            clean_results.append(
                {
                    "url": result["url"],
                    "content": result["content"],
                }
            )
        return clean_results
