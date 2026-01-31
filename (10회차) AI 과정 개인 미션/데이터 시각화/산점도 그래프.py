import seaborn as sns
import matplotlib.pyplot as plt

# 샘플 데이터 로드 (붓꽃 데이터)
df = sns.load_dataset('iris')

# 산점도: 꽃받침 길이와 너비의 관계
sns.scatterplot(x='sepal_length', y='sepal_width', hue='species', data=df)
plt.title('Sepal Length vs Width')
plt.show()

# 산점도 행렬: 모든 변수 간의 관계
sns.pairplot(df, hue='species')
plt.suptitle('Pairplot of Iris Dataset', y=1.02)
plt.show()

# 조인트플롯: 꽃잎 길이와 너비의 관계
sns.jointplot(x='petal_length', y='petal_width', data=df,
                kind='scatter', hue='species')
plt.suptitle('Petal Length vs Width', y=1.02)
plt.show()

# 래그플롯: 꽃받침 길이와 너비의 관계
sns.lmplot(x='sepal_length', y='sepal_width', hue='species', data=df)
plt.title('Sepal Length vs Width with Regression Line')
plt.show()

# 헥스빈 플롯: 꽃잎 길이와 너비의 밀도
sns.jointplot(x='petal_length', y='petal_width', data=df,
                kind='hex')
plt.suptitle('Hexbin Plot of Petal Length vs Width', y=1.02)
plt.show()

# 케이스별 산점도: 종별 꽃받침 길이와 너비의 관계
g = sns.FacetGrid(df, hue='species', height=5)
g.map(sns.scatterplot, 'sepal_length', 'sepal_width')
g.add_legend()
plt.title('Sepal Length vs Width by Species')
plt.show()