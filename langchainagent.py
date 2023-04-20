# create a langchain agant to search google scholar

from langchainagent import LangChainAgent
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import faiss
import os
import json
import requests
import re
import time
import random
import string
import sys
import logging

OPENAI_API_KEY = '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'


class GoogleScholarAgent(LangChainAgent):
