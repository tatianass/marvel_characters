from marvel_characters.main import main


class TestMarvelCharacters:
    def test_main(self):
        result = main()
        assert result == "Process finished!"
