from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
    You are a highly capable assistant trained to analyze and summarize documents.
    Return ONLY using valid JSON matching the exact schema below:
    
    {format_instructions}

    Analyze the document:

    {document_text}
    """ 
)