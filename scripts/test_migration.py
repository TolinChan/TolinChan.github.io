#!/usr/bin/env python3

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from migrate_wordpress import (  # noqa: E402
    internal_archive_path,
    mysql_unescape,
    rewrite_internal_urls,
    route_for_post,
)


class MigrationHelpersTest(unittest.TestCase):
    def test_rewrites_internal_hosts_and_toc(self) -> None:
        source = (
            '<img src="http://116.62.4.97/wp-content/uploads/a.jpg">'
            '<a href="http://blog.tolinchan.xyz/about/">about</a>[toc]'
        )
        result = rewrite_internal_urls(source)
        self.assertNotIn("116.62.4.97", result)
        self.assertNotIn("http://blog.tolinchan.xyz", result)
        self.assertIn('/wp-content/uploads/a.jpg', result)
        self.assertIn('data-auto-toc', result)

    def test_accepts_only_internal_upload_paths(self) -> None:
        self.assertEqual(
            internal_archive_path(
                "http://116.62.4.97/wp-content/uploads/2024/01/a.jpg"
            ),
            "wp-content/uploads/2024/01/a.jpg",
        )
        self.assertIsNone(internal_archive_path("https://example.com/a.jpg"))
        self.assertIsNone(
            internal_archive_path("http://116.62.4.97/wp-content/../wp-config.php")
        )

    def test_decodes_legacy_chinese_slug(self) -> None:
        xml = """
        <item xmlns:wp="http://wordpress.org/export/1.2/">
          <wp:post_id>1</wp:post_id>
          <wp:post_date>2024-03-04 12:00:00</wp:post_date>
          <wp:post_name>%e6%b5%8b%e8%af%95</wp:post_name>
        </item>
        """
        self.assertEqual(route_for_post(ET.fromstring(xml)), "/2024/03/04/测试/")

    def test_mysql_escape_decoding(self) -> None:
        self.assertEqual(mysql_unescape(r"line\nquoted\'"), "line\nquoted'")


if __name__ == "__main__":
    unittest.main()
