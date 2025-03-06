from marvel_characters.generate_raw_data import main


class TestMarvelCharacters:
    def test_main(self):
        result = main()
        assert result == "Process finished!"
