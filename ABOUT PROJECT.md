# Health Chatbot: A Retrieval Agumented Generation (RAG) Chatbot with Topic Classification


## Domain Proyek
This RAG (Retrieval Agumented Generation)-based chatbot is designed to provide information on three key topics: medications, menstruation, and allergies. By integrating topic classificaition, the chatbot understands user topics and then retrieves relevant information based on the proposed topic before generating an answer using a generative model like GPT. With these capabilities, the chatbot can accruately answer question related to these three topics.

## Business Understanding
### Problem Statements
- How can the chatbot effectively classify the topic of user prompts?
- How can the chatbot provide response to questions related to these three topics? 
- How can we integrate a RAG-based search system with topic classification to improve response quality

### Goals
The project goals to enhance accuracy in answering health-related questions, spesifically medical information about medications, mentrual issues, and allergies, using AI-based language modeling techniques. The information used by the chatbot is sourced from trusted website that provide Q&A services about these topics.

### Solution Statements
To achieve these goals, we'll first find a reliable and validatable dataset. This data will serve as the chatbot's knowledge base and for training the topic classification model.

For topic classification, we've chosen the IndoBERT model [[1]](https://huggingface.co/indobenchmark/indobert-base-p1).The model is fine-tuned using a dataset crawled from a health website, containing over 14.000 rows with two features: "intent" and "question". For the RAG process, we're using ChromaDB as the knowledge base storage abd GPT-3.5-Turbo as the generative model

## Data Understanding
The dataset consists of over 14,000 rows, manually collected through web crawling from an Indonesian health service website.

Data preprocessing ensures the dataset is ready for model training and chatbot knowledge base. First, we transform text to lowercase for data consistency. Then we remove unnecessary punctuation and characters. Some crawled rows had null values and were removed. We also found duplicate data, likely due to staged crawling.

The preprocessed dataset is split into two. The first is used for fine-tuning IndoBERT for intent classification, using only the 'intent' and 'question' columns. The second serves as the chatbot's knowledge base, also using 'intent' and 'answer' columns.


## Data Preparation
Preparation focuses on the first dataset for topic classification. Labels in the 'topic' column are mapped as follows:

- Label 0 for 'allergy' topic
- Label 1 for 'medication' topic
- Label 2 for 'menstruation' topic


## Modeling
Two key stages: intent classification and RAG.
### Intent Classification
We use IndoBERT [[1]](https://huggingface.co/indobenchmark/indobert-base-p1), fine-tuned on the first dataset. Fine-tuning involves training the last layer of IndoBERT to adapt to the specific task of intent classification. We replace the classification layer to predict three intent classes: medication, menstruation, and allergy. The process uses AdamW optimization and appropriate loss functions.

### Retrieval Augmented Generation (RAG)
RAG involves retrieval and generation processes to enhance the chatbot's ability to provide answers beyond predictive models.

We convert the knowledge base to vectors using the SentenceTransformers all-MiniLM-L6-v2 model [[2]](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) and store them in ChromaDB. Generative tasks are handled by GPT-3.5-Turbo, with the entire RAG process supported by LangChain.


### Topic Classification and RAG Integration
The system workflow:

1. Receive user prompt
2. Pass prompt to fine-tuned IndoBERT for topic classification
3. Search for relevant information based on intent and user prompt
4. Send retrieved information to GPT-3.5-Turbo for response generation


## Evaluation
We used quantitative and qualitative evaluation techniques.
Quantitative evaluation for topic classification:

- Accuracy: 94%
- Recall: 94%
- Precision: 94%
- F1-score: 94%

RAG evaluation was qualitative. Results showed 80% of questions were answered well. Some challenges include diverse knowledge bases making similarity calculations difficult, and variations in prompt and knowledge base lengths.

## Recommendation
For similar projects:

- Closely monitor web crawling to ensure dataset relevance
- Enhance preprocessing to remove irrelevant information
- Implement evaluation metrics like BLEU, ROUGE-1, ROUGE-2 for RAG processes

## Additional Resource
- Fine tuned IndoBERT model, can access in here [[CLICK HERE]](https://huggingface.co/iqbalpurba26/IndoBERT_intent_classification).
- Dataset not publicly available. For collaboration, contact via LinkedIn: [CLICK HERE](https://www.linkedin.com/in/m-iqbal-purba)