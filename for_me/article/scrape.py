import pandas as pd 

hn_df = pd.DataFrame(data=None, columns=['type', 'title', 'url'])

for num in range(0,6):
	file_name = 'output%s' % num + '.csv'
	df = pd.read_csv(file_name)
	df = df[(df.type == 'story')]
	df = df.drop(['time', 'score', 'id', 'by', 'text'], axis=1)
	hn_df = hn_df.append(df, ignore_index=True)	

hn_df = hn_df[hn_df.title.notnull() & hn_df.url.notnull()]
print(hn_df)

# Classifying each of the articles with regex




# Python	python|pandas
# Mobile	mobile|android|iphone|phone
# Design	design
# Security	security|worm|ransomware|attack|virus|patch|infosec
# Blockchain	blockchain|bitcoin|ethereum
# AI/Machine Learning	\bai\b|artificial intelligence|machine learning|deep learning|tensorflow|machine intelligence
# Google	google
# Microsoft	microsoft|windows|visual studio
# Apple	apple|mac\b|os ?x
# Facebook	facebook
# Amazon	amazon
# Startups	startup|\bvc\b
# Politics	trump|comey|russian|fbi|snowden|neutrality|white house|government|brexit|nsa
# Databases	sql|cockroachdb|mongodb|database|\bdb\b
# Linux	linux|debian|ubuntu|centos
# Data Science	data scien|big data|data vi|data ?set|data analy|machine learning|pandas|ggplot2
# Science	bio|drug|researcher|genomic|physics|scienti|spacex|\\bmoon\\b|nasa|\\bastro|\\bmars\\b
# Math	math|geome|cryptograph|algebra|calculus