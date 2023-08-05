from unittest import TestCase

from chibi.file import inflate_dir, join


class Test_join( TestCase ):

    def setUp( self ):
        self.root = '/'
        self.home = inflate_dir( '~' )

    def test_double_root_is_only_root( self ):
        self.assertEqual( join( self.root, self.root ), join( self.root ) )

    def test_home_and_current_should_end_combined( self ):
        result = join( self.home, 'qwert' )
        self.assertTrue( result.startswith( self.home ) )
        self.assertTrue( result.endswith( 'qwert' ) )
