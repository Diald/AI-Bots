The repository contains a common directory for all the new AI frameworks and topics i have tried using. This is just for my personal reference. 

1. Orchestrator Agent -
   template of how mcp servers can be written and made, used gemini2.5 for the llm part and the llm basically decides which tool to use based on the input provided. for example
   if the use cases requires to run tool1 the llm analyses the use case and based on that defines which tool would be suitable, a very good use case for agentic ai's i would
   say.
2. RAG Agent -
   As the name suggests, RAG system is used to implement this, it is a very basic template which is like a code analyzer, it basically ingests a file and then you can ask any
   question from within the file. for example you could provide it a txt or pdf file that contains information about 'INDIA' and then you can ask it anything about INDIA. It is
   a very useful use case if any entriprise want to provide model about information that is not present over the internet and they wanna build an agent that knows confidential
   data. It could be seen as a mini training your model.
3. RAGLangchain -
   similar but have used Langchain for this, wanted to try langchain
4. security_agent -
   as a cybersecurity personnel i wanted to build an agent that could do scanning for me, all the sast, dast, secret scanning, i moved it to a bigger project -
   https://github.com/Diald/security-agent, so basically the input would be a github url and then the project would scan the repository and scan for any vulnerabilities, if it
   have any outdated end of life libraries, any personal libraries or any leaked secret and then llm finally generates a report of all the findings.
