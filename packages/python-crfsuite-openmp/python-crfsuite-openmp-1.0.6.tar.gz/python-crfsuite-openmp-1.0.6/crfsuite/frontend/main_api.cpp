#include <os.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "option.h"
#include <crfsuite.h>
#include <crfsuite.hpp>


#define    APPLICATION_S    "CRFSuite"

using namespace CRFSuite;


int main(int argc, char *argv[])
{


	// Teste
	Trainer * trainer = new CRFSuite::Trainer();

	ItemSequence c_seq;

	Item item;
	item.push_back(Attribute("OI", 1));
	c_seq.push_back(item);

	trainer->append(c_seq);




	return 0;

}
