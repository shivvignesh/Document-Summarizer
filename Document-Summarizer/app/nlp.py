from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration
)

class NLP:
    def __init__(self):
        self.summary_tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.summary_model = T5ForConditionalGeneration.from_pretrained('t5-base')
         

    def summary(self,text: str):
        self.summary_model.eval()
        inputs = self.summary_tokenizer.encode("summarize"+text,
                                                return_tensors="pt",
                                                max_length=512,
                                                truncation=True)

        summary_ids = self.summary_model.generate(inputs,min_length=60,max_length=180,length_penalty=6.0)
        print(summary_ids)
        summary = self.summary_tokenizer.decode(summary_ids[0])

        return summary



    

    