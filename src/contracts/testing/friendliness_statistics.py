from contracts.test_registrar import (good_examples, semantic_fail_examples,
                                      contract_fail_examples)
from contracts import parse, ContractSyntaxError

def get_all_strings():
    all = (good_examples + semantic_fail_examples + contract_fail_examples)
    for contract, value, exact in all: #@UnusedVariable
        if isinstance(contract, list):
            for c in contract:
                yield c
        else:
            yield contract

# went from 89.9% to 95.7%
 
def main():
    examples = get_all_strings()
    
    differences = run_joker(examples)
    
    import numpy
    unfriendliness = numpy.mean(list(differences))

    friendliness = 100 - 100 * unfriendliness
    print "Friendliness: %.2f%% " % friendliness  
    

def replace_one(s, i, c):
    assert i >= 0 and i < len(s)
    return s[:i] + c + s[i + 1:]

assert replace_one('python', 1, 'a') == 'pathon'
s = 'python'
for i in range(len(s)):
    s2 = replace_one(s, i, '~')
    s3 = replace_one(s2, i, s[i])
    assert s == s3, 'i=%d  %r -> %r -> %r' % (i, s, s2, s3)

def run_joker(examples):
    
    for s in examples:
        # make sure we can parse it
        parse(s)
        
        # now alter one letter
        for i in range(len(s)):
            s2 = replace_one(s, i, '~')
            
            try: 
                parse(s2)
                
            except ContractSyntaxError as e:
                detected = e.where.col - 1
                displacement = i - detected
#                if  displacement < 0:
#                    print displacement
#                    print e 
                assert displacement >= 0

                value = displacement * 1.0 / len(s)
                if displacement > 5:
                    print e
#                    assert False
                    
                yield value
            


if __name__ == '__main__':
    main()
