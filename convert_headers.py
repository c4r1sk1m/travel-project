import json
def main():
    print("Enter Headers File: ")
    filename = input()
    outputMap = {}
    with open(filename,"r") as file:
        firefoxHeaders = json.load(file)
        topKey = list(firefoxHeaders.keys())[0]
        for header in firefoxHeaders[topKey]["headers"]:

            outputMap[header['name']] = header['value']
    print("Enter output filename: ")
    outfileName = input()
    with open(outfileName,'w',encoding='utf-8') as outfile:
        json.dump(outputMap, outfile,ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()