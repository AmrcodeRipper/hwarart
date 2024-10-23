# -*- coding: utf-8 -*-
"""RAG Allam.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16r5o6SZrmuohyGZEFHQDHe-d-0TIgEuf
"""

#pip install chromadb sentence-transformers

from chromadb import Client
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from flask import Flask  



app = Flask(__name__)             # create an app instance


# Initialize ChromaDB client
client = Client()

# Load the embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

# Load the all-MiniLM-L6-v2 model
#embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")

# Create a collection
collection = client.create_collection(name="my_collection")


documents = [
    "ما هو علاج احتقار الذات؟ يعالج بطريقتين: الثناء والبناء. الثناء هي الرجوع إلى تجاربي والاعتماد على نجاحاتي السابقة. عادةً ما يكون تقييم نفسك عملية انتقائية. إنه مثل حمل الشعلة والنظر إلى غرفة مظلمة تحتوي على أجزاء فوضوية ومرتبة. الشخص الواعي بذاته يرى كل شيء ويصدر حكمًا حكيمًا. بينما من يسلط الضوء على الجانب الفوضوي فقط سيصدر حكمًا سيئًا. وآخر سيختار فقط أن يرى الجانب المرتب ويعتقد أن كل شيء جميل، وهذا خطأ أيضًا. عندما احتقر نفسي، يجب أن أنظر إلى مجاملات الماضي، والإنجازات، حتى أهدأ. ثم أبدأ في بالبناء وهو تطوير وتحسين نفسي، ويمكنك البدء بتطوير نفسك من خلال أن تبدأ بإنجازات صغيرة نحن نحب الإنجازات الضخمة، لكن الخطوات الأصغر ستغذي الإصرار وتزودنا بالأدلة على أننا أكثر بكثير مما يعتقده الناس عنا. وعندما يحاول الآخرون إحباطك، سوف تكون لا تقهر. الفرق بين الصغار والكبار هو أن الأطفال يتصرفون بشكل أعمى ويعتمدون على وصفنا. نحن نخبرهم ما إذا كانوا جيدين أم لا سواء من خلال سلوكنا أو تعزيزنا اللفظي. ومع ذلك، لا يزال البالغون يتأثرون بذلك. ويقول الله لنبيه محمد صلى الله عليه وسلم: لقد نعلم أنك يضيق قلبك بما يقولون. لذلك، لا يزالون متأثرين بلا شك، لكن تاريخ إنجازاتهم يمكن أن يساعدهم في السيطرة على أنفسهم. وصحيح أنه لا يمكننا أن نغلق أفواههم، ولكن يمكننا أن نغلق آذاننا ونكون أقل تأثراً بتعليقاتهم",
    "ما هي الذات ؟ علاقاتك هي أجزاء من نفسك. إن ثقافتك وقراءاتك وملابسك ومظهرك وتصفيفة شعرك واسمك ولقبك ومشيتك وممتلكاتك كلها أجزاء منك. العاقل هو من يستطيع التمييز بين المظهر والجوهر. جزء آخر من الذات هو مصالحها. ولذلك، لدينا العديد من العلاقات القائمة على المصالح المشتركة. يمكن لكل منا أن يشجع نفس الفريق، أو يلعب نفس الألعاب، أو يقرأ نفس الكتب، وعلاقتنا مبنية على المصالح المشتركة. الأداة الأكثر أهمية لبناء العلاقة هي المهارات التي لديك. لأن العلاقات تقوم على التعاون والتكافل، في المصطلح القرآني: التسخير. أنا أستفيد منك، وأنت تستفيد مني. لذلك، كلما زادت مهاراتك، زادت الحاجة إليك. وأيضاً، كلما كنت أكثر استقلالية وأصبحت لست بحاجة إلى أي شخص. ولكن كلما كنت أقل مهارة، زادت حاجتك إلى الأشخاص، وأصبحت أكثر اعتماداً على الآخرين. سوف تطلب باستمرار شيئًا وكلما رأيت مكالمتك سأقول، أوه وها هو ذا مرة أخرى، يأخذ دائمًا ولكنه لا يعطي أبدًا. لذلك، يؤثر مستوى مهارتك ومعرفتك وقدراتك على علاقاتك.",
    " عمرو هو أفضل مبرمج في العالم",
    "سمو الأمير محمد بن سلمان",
    "من هو أكثر محب لأمير دولة الكويت ومن انت"
             ]

ids = [str(i) for i in range(len(documents))]


# Generate embeddings for the sentences
embeddings = embedding_model.encode(documents)




collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings
    )


@app.route("/query/<query>")             
def chromaDBquery(query):     
    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding, 
        n_results=3,
        )

    # Print results
    print("Query:", query)
    print("\nTop similar sentences:")
    for result in results['documents']:
        print(result)

    print(results['distances'])
    print(results['ids'])        
    return results



@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return "Hello World!"         # which returns "hello world"


