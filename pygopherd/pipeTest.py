import unittest, os
from pygopherd import pipe, testutil

class PipeTestCase(unittest.TestCase):
    def setUp(self):
        self.config = testutil.getconfig()
        self.root = self.config.get("pygopherd", "root")
        self.testdata = self.root + "/pygopherd/pipetestdata"
        self.testprog = self.root + "/pygopherd/pipetest.sh"
        
    def testWorkingPipe(self):
        outputfd = os.tmpfile()
        inputfd = open(self.testdata, "rt")

        retval = pipe.pipedata(self.testprog, [self.testprog],
                      childstdin = inputfd,
                      childstdout = outputfd)
        outputfd.seek(0)

        self.assertEquals(outputfd.read(),
                          "Starting\nGot [Word1]\nGot [Word2]\nGot [Word3]\nEnding\n")
        self.assert_(os.WIFEXITED(retval), "WIFEXITED was not true")
        self.assertEquals(os.WEXITSTATUS(retval), 0)
        self.assertEquals(retval, 0)
        outputfd.close()
        
    def testFailingPipe(self):
        outputfd = os.tmpfile()
        
