"""Tests for TablePromptResponse."""
import unittest

from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestTablePromptResponse(unittest.TestCase):
    """Test cases for TablePromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.headers = ["Name", "Age", "City"]
        self.data = [
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"],
            ["Bob", "35", "Chicago"]
        ]
        
    def test_create_table_with_headers(self):
        """Test table creation with separate headers."""
        table = TablePromptResponse.create_table(
            data=self.data,
            headers=self.headers,
            context=self.context
        )
        rendered = table.render()
        
        # Check header
        self.assertIn("Name", rendered)
        self.assertIn("Age", rendered)
        self.assertIn("City", rendered)
        
        # Check data
        self.assertIn("John", rendered)
        self.assertIn("30", rendered)
        self.assertIn("New York", rendered)
        
    def test_create_table_without_headers(self):
        """Test table creation without headers."""
        table = TablePromptResponse.create_table(
            data=self.data,
            context=self.context
        )
        rendered = table.render()
        
        # Check data is present without headers
        self.assertIn("John", rendered)
        self.assertIn("30", rendered)
        self.assertIn("New York", rendered)
        
    def test_empty_table(self):
        """Test empty table handling."""
        table = TablePromptResponse.create_table(
            data=[],
            context=self.context
        )
        rendered = table.render()
        self.assertEqual(rendered.strip(), "")
        
    def test_single_column(self):
        """Test single column table."""
        data = [
            ["Row 1"],
            ["Row 2"]
        ]
        headers = ["Header"]
        table = TablePromptResponse.create_table(
            data=data,
            headers=headers,
            context=self.context
        )
        rendered = table.render()
        self.assertIn("Header", rendered)
        self.assertIn("Row 1", rendered)
        self.assertIn("Row 2", rendered)
        
    def test_table_with_title(self):
        """Test table with title."""
        title = "Employee List"
        table = TablePromptResponse.create_table(
            data=self.data,
            headers=self.headers,
            title=title,
            context=self.context
        )
        rendered = table.render()
        self.assertIn(title, rendered)
        self.assertIn("John", rendered)
        
    def test_column_alignment(self):
        """Test that columns are properly aligned."""
        table = TablePromptResponse.create_table(
            data=self.data,
            headers=self.headers,
            context=self.context
        )
        rendered = table.render()
        lines = rendered.split('\n')
        
        # Find lines with data
        data_lines = [line for line in lines if any(name in line for name in ["John", "Jane", "Bob"])]
        
        # Get positions for each column
        name_positions = [line.find("John" if "John" in line else "Jane" if "Jane" in line else "Bob") for line in data_lines]
        age_positions = [line.find("30" if "30" in line else "25" if "25" in line else "35") for line in data_lines]
        city_positions = [line.find("New York" if "New York" in line else "San Francisco" if "San Francisco" in line else "Chicago") for line in data_lines]
        
        # Check that each column starts at consistent positions
        self.assertEqual(len(set(name_positions)), 1, "Names should be aligned in the same column")
        self.assertEqual(len(set(age_positions)), 1, "Ages should be aligned in the same column")
        self.assertEqual(len(set(city_positions)), 1, "Cities should be aligned in the same column")
        
        # Verify column order
        self.assertTrue(all(name_pos < age_pos < city_pos for name_pos, age_pos, city_pos in 
                          zip(name_positions, age_positions, city_positions)), 
                          "Columns should be in order: Name, Age, City")
