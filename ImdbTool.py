"""Tool for the Imdb search API."""

from typing import Dict, List, Optional, Type, Union

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
from ImdbApiWrapper import ImdbSearchAPIWrapper

class ImdbInput(BaseModel):
    """Input for the Imdb tool."""

    query: str = Field(description="search query to look up.")

class ImdbQuery(BaseTool):
    """Tool that queries the Imdb Search API and gets back json."""

    name: str = "imdb_search_results_json"
    description: str = (
        "A search engine tailored for delivering comprehensive, precise, and reliable results. It excels in providing up-to-date information, making it indispensable for addressing inquiries about current events. Ensure that your input consists solely of a search query string. Remember, the returned data is a stringified JSON object, necessitating meticulous filtering to extract movie details accurately. It's crucial to emphasize that movie information might be available in languages other than English, so be prepared to translate if necessary. Stick to the provided movie list exclusively; do not consider any other options. Craft your search query parameter strictly in the format: query: 'action,drama,suspense,...', listing genres separated by commas with no additional elements. Consistency and accuracy hinge on adhering to these guidelines."
    )
    api_wrapper: ImdbSearchAPIWrapper = Field(default_factory=ImdbSearchAPIWrapper)
    max_results: int = 5
    args_schema: Type[BaseModel] = ImdbInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            return self.api_wrapper.results(
                query,
                self.max_results,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously."""
        try:
            return await self.api_wrapper.results_async(
                query,
                self.max_results,
            )
        except Exception as e:
            return repr(e)