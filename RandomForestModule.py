import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier #Decision Tree algoritmasının çok katmanlı kullanımlarda kullananan modelleme
from sklearn.model_selection import train_test_split #data eğitimi için kütüphaneden çağılma işlemi
from sklearn import metrics

DATA = "E:\DATA"

CATEGORIES = ["Fire","Forrest"]

for category in CATEGORIES : #
    path = os.path.join(DATA,category) #yangın ve orman için tüm imgleri patch içine alır
    for img in os.listdir(path): #her img array haline çevirme
        img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE) #grileştirme de yapıldı.
        plt.imshow(img_array,cmap = 'gray') # grafiklertieme
        #plt.show()

        break
    break

#print(img_array.shape)#kaç satır kaç sütüun yazdırma.
IMG_SIZE = 100

new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
#plt.show()
# üstte datalarımızı array ve gray uygun hale getirdik.şimdi data eğitimi yapcağız.

training_data = []
def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATA,category)
        class_num = CATEGORIES.index(category) #sınıflandırma yapıyoruz. 0=yangın,1=orman(yangınsız)
        for img in os.listdir(path):  # her img array haline çevirme
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)  # grileştirme de yapıldı.
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                image = np.array(new_array).flatten()
                training_data.append([image,class_num])
            except Exception as e:
                pass

create_training_data()

#print(len(training_data))

random.shuffle(training_data)
X = []
y = []

for features,label in training_data:
    X.append(features)
    y.append(label)


#print(X)
#print(y)
'''
X = np.array(X)
X_2d = X.ravel()
y=np.array(y)
y_2d =y.ravel()
print(X_2d.shape)
print(y.shape)
'''

clf=RandomForestClassifier()#algoritmayı clf atadık
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)
#metrics scores
y_pred = clf.predict(X_test)
y_pred_prob=clf.predict_log_proba(X_test)[:,1]
acc = metrics.accuracy_score(y_test, y_pred)
auc_score = metrics.roc_auc_score(y_test,y_pred)
MCC =metrics.matthews_corrcoef(y_test,y_pred)
F_REC_Pre = metrics.classification_report(y_test,y_pred,target_names=CATEGORIES)
#değerleri yazdırma
print("Sınıfı : ",CATEGORIES[y_pred[1]])
print("Accuracy:",acc)
print("AUC score :",auc_score)
print("Mathew Correlation Coefficient : ",MCC)
print(F_REC_Pre)
#etiketli fotoyu gösterme
sınıf =X_test[2].reshape(IMG_SIZE,IMG_SIZE)
plt.imshow(sınıf,cmap='gray')
plt.show()