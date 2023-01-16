# encoding : utf-8

import os,json

def main():
	collectList = []
	for i in os.listdir("rubbishData"):
		collectList.append(
			json.loads(
				open("rubbishData\\"+i,"r",encoding="utf8").read()
				)
			)
	collectRange = {
		"comman" : [],
		"manner" : [],
		"rubbish" : []
	}
	for i in collectList:
		for j in i["comman"]:
			if j not in collectRange["comman"]:
				collectRange["comman"].append(j)
		for j in i["manner"]:
			if j not in collectRange["manner"]:
				collectRange["manner"].append(j)
		for j in i["rubbish"]:
			if j not in collectRange["rubbish"]:
				collectRange["rubbish"].append(j)
	open("rubbishCollect.json", "w", encoding="utf-8").write(json.dumps(collectRange))

if __name__ == '__main__':
	main()