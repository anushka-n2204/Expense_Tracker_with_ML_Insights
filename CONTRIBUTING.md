# Contributing to Smart Expense Tracker

Thank you for considering contributing to this project!

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in Issues
- Include detailed steps to reproduce
- Include screenshots if applicable
- Specify your Python version and OS

### Suggesting Enhancements
- Open an issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Include mockups or examples if possible

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow PEP 8 style guide
   - Add docstrings to functions
   - Comment complex logic
4. **Test your changes**
   ```bash
   python test_setup.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-expense-tracker.git
cd smart-expense-tracker

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_setup.py

# Run the app
streamlit run app.py
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused
- Use type hints where appropriate

## Testing

- Test all new features manually
- Ensure existing functionality still works
- Test on different screen sizes
- Test edge cases (empty data, large datasets, etc.)

## Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Update documentation if needed
- Include screenshots for UI changes
- Reference related issues
- Ensure all tests pass

## Feature Ideas

Here are some features that would be great additions:

- **Recurring Expenses**: Auto-add monthly subscriptions
- **Category-wise Budgets**: Set budgets per category
- **Multi-currency Support**: Support for different currencies
- **Data Visualization**: More chart types and insights
- **Export Formats**: PDF, Excel support
- **Mobile Responsive**: Better mobile UI
- **Dark Mode**: Theme toggle
- **Search**: Advanced search and filters
- **Tags**: Add custom tags to expenses
- **Notes**: Add notes/comments to expenses

## Questions?

Open an issue with the "question" label or reach out to the maintainers.

Thank you for contributing! 🎉
