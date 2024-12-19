import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author("John Doe", 1)
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article("Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Tech Weekly")
        self.assertEqual(magazine.name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()
