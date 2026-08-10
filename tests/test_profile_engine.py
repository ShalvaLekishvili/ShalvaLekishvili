import json
import tempfile
import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import profile_engine as pe

class ProfileEngineTests(unittest.TestCase):
    def setUp(self):
        self.config=pe.load_json(ROOT/'config/portfolio.json')
        self.live=pe.load_json(ROOT/'data/baseline.json')

    def test_credential_count(self):
        self.assertEqual(len(self.config['credentials']), 14)
        self.assertEqual(sum(c['provider']=='TryHackMe' for c in self.config['credentials']), 10)

    def test_claim_summary(self):
        self.assertEqual(pe.claim_summary(self.config,self.live), (6,6))

    def test_dark_and_light_svg(self):
        for theme in ('dark','light'):
            svg=pe.render_live_intelligence(self.config,self.live,theme)
            self.assertIn('<svg',svg)
            self.assertIn('SentinelForge',svg)
            self.assertIn('PacketScope',svg)
            self.assertIn('CLAIMS VERIFIED 6/6',svg)

    def test_semantic_snapshot_ignores_generated_at(self):
        a={"generated_at":"a","source":"x","api_version":"1","repos":{"r":{"stars":1}}}
        b={"generated_at":"b","source":"x","api_version":"1","repos":{"r":{"stars":1}}}
        self.assertEqual(pe.semantic_snapshot(a), pe.semantic_snapshot(b))

    def test_credential_svg_contains_ids(self):
        svg=pe.render_credential_matrix(self.config,'dark')
        self.assertIn('THM-TH8U8ODRGS',svg)
        self.assertIn('14 DOCUMENTED PROGRAMS',svg)

if __name__=='__main__': unittest.main()
