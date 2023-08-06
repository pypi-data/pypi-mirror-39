import unittest
import time

import sbrowser


class TestBrowser(unittest.TestCase):

    def testRequest(self):
        data = sbrowser.goto("https://www.uni-hannover.de")
        self.assertTrue(len(data) > 1000)
        self.assertTrue("Leibniz" in str(data))
        self.assertTrue("impressum" in str(data))

    def testTimeout(self):
        currTime = time.perf_counter()
        sbrowser.goto("https://www.uni-hannover.de")
        sbrowser.goto("https://www.uni-hannover.de")
        afterTime = time.perf_counter()
        self.assertTrue((afterTime-currTime) > 3)

    def testMethod(self):
        try:
            sbrowser.goto("https://www.uni-hannover.de", method="WHAT")
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def testLastURL(self):
        sbrowser.goto("http://uni-hannover.de")
        self.assertEqual(sbrowser.lasturl, "https://www.uni-hannover.de/")
