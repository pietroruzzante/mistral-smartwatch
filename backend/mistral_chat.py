from mistralai import Mistral

class MistralChat:
    """
    This class manages a chat with Mistral AI, storing messages and calling Mistral API.

    attributes:
        - client: a Mistral's class object with user's api key
        - model: str
            A string describing the model, defined as Mistral documentation states
        - messages: list
            A list of messages which contains chat history
    """
    def __init__(self, api_key, model):
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.messages = []

        # initialize chat with system prompt
        self.messages.append({"role": "system",
                              "content": "You are a helpful assistant for analyzing smartwatch data. Please return your analysis in Markdown."
                              })

    def new_message(self, new_message):
        """
        Appends a new message to the chat, invoke Mistral API and return the response.
        param
            new_message: str
                new user's message
        return:
            answer: str
                model's answer
        """
        # append a new message to chat
        self.messages.append({"role": "user", "content": new_message})
        # LLM calling
        chat_response = self.client.chat.complete(model=self.model, messages=self.messages)
        answer = chat_response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})

        return answer

