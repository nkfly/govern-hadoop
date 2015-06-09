#include <iostream>
#include <stdio.h>
#include <string.h>
#include <string>
#include <vector>
using namespace std;

class CatNode {
    public:
      CatNode(string _catName) {
        catName = _catName;
        merchandiseCount = 0;
      }
      void addMerchandiseCount();
      int getMerchandiseCount();
      CatNode* getChild(int id);
      int addChild(string catName);
      int getChildNum();
      string getCatName();
    private:
      string catName;
      int merchandiseCount;
      vector<CatNode*> child;

};

void CatNode::addMerchandiseCount() {
	merchandiseCount++;
}

int CatNode::getMerchandiseCount() {
	return merchandiseCount;
}

CatNode* CatNode::getChild(int id) {
	return child[id];
}

int CatNode::addChild(string catName) {
	CatNode* cn = new CatNode(catName);
	child.push_back(cn);
	return child.size() - 1;
}

int CatNode::getChildNum() {
	return child.size();
}

string CatNode::getCatName() {
    return catName;
}

void constructTree(CatNode* cn, char* cat, int first);
void dumpTree(CatNode* root, int layer);
int main() {
    FILE *fp;
    fp = fopen("view.csv", "r");
    char line[1000];
    if (!fp) {
        cout << "file open error." << endl;
    }
    fscanf(fp, "%s\n", line);
    int i;
    int dot;
    int index;
    CatNode* root = new CatNode("ROOT");
    while (fgets(line, 1000, fp) != NULL) {
        char cat[500] = {'\0'};
	dot = 0;
	index = 0;
        for (i=0 ; i<strlen(line) ; i++) {
	    if (line[i] == ',') {
	        dot++;
		continue;
	    }
	    if (dot == 9) {
	        if (line[i] == ',') {
	            cat[index] = '\0';
		    break;
		}
                cat[index++] = line[i];
	    }
	}
	char temp[500];
	strcpy(temp, cat);
        char* tok[50];
	int tokNum = 0;
	tok[tokNum++] = strtok(temp, "-");
	while (true) {
	    tok[tokNum++] = strtok(NULL, "-");
	    if (tok[tokNum-1] == NULL) {
	        constructTree(root, tok[tokNum-2], 1);
		break;
	    }
	}
    }
    dumpTree(root, 0);
}

void constructTree(CatNode* cn, char* cat, int first) {
    cn->addMerchandiseCount();
    char* tok;
    if (first) {
        tok = strtok(cat, "_");
    } else {
	tok = strtok(NULL, "_");
    }
    if (tok == NULL) {
        return;
    }
    int i;
    bool find = false;
    for (i=0 ; i<cn->getChildNum() ; i++) {
        CatNode* cnChild = cn->getChild(i);
	string catName = cnChild->getCatName();
	if (catName.compare(tok) == 0) {
            constructTree(cnChild, cat, 0);
	    find = true;
	    break;
	}
    }
    if (!find) {
	string catName(tok);
	int childIndex;
	childIndex = cn->addChild(catName);
        constructTree(cn->getChild(childIndex), cat, 0);
    }
    
}

void dumpTree(CatNode* cn, int layer) {
    int i;
    for (i=0 ; i<layer ; i++) {
        cout << "-";
    }
    cout << cn->getCatName() << " ";
    cout << cn->getMerchandiseCount() << endl;
    for (i=0 ; i<cn->getChildNum() ; i++) {
        dumpTree(cn->getChild(i), layer+1);
    }
}














