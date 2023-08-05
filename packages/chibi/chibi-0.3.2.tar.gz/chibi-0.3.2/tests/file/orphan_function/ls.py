from tests.snippet.files import Test_with_files
from chibi.file import ls


class Test_ls( Test_with_files ):
    def test_should_list_all_the_files_and_dirs_from_root( self ):
        result = list( ls( self.root_dir ) )
        self.assertTrue(
            len( result ) == ( self.amount_of_dirs + self.amount_of_files ) )

    def test_should_return_a_empty_list( self ):
        result = list( ls( self.empty_folder ) )
        self.assertFalse( result )
