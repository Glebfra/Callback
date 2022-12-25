from kivy.app import App
from kivy.uix.widget import Widget
from random import choice, randint
from kivent_core.gameworld import GameWorld
from kivent_core.managers.resource_managers import texture_manager
from os.path import dirname, join, abspath
from kivent_core.systems.gamesystem import GameSystem
from kivent_maps import map_utils
from kivent_maps.map_system import MapSystem

def get_asset_path(asset, asset_loc):
    return join(dirname(dirname(abspath(__file__))), asset_loc, asset)

class TestGame(Widget):
    def on_kv_post(self, *args):
        self.gameworld.init_gameworld(
            ['map_layer0', 'position', 'camera1', 'map_layer0_animator',
             'tile_map'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.load_textures()
        self.load_models()
        self.load_animations()
        self.set_state()
        self.setup_tile_map()

    def load_textures(self):
        texture_manager.load_image(get_asset_path('orange-tile.png', 'assets'))
        texture_manager.load_image(get_asset_path('purple-tile.png', 'assets'))
        texture_manager.load_image(get_asset_path('green-tile.png', 'assets'))
        texture_manager.load_image(get_asset_path('blue-tile.png', 'assets'))

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle('vertex_format_4f', 64., 64.,
                                              'orange-tile', 'orange-tile')
        model_manager.load_textured_rectangle('vertex_format_4f', 64., 64.,
                                              'purple-tile', 'purple-tile')
        model_manager.load_textured_rectangle('vertex_format_4f', 64., 64.,
                                              'green-tile', 'green-tile')
        model_manager.load_textured_rectangle('vertex_format_4f', 64., 64.,
                                              'blue-tile', 'blue-tile')

    def load_animations(self):
        animation_manager = self.gameworld.animation_manager
        frames = [{
            'texture': 'orange-tile',
            'model': 'orange-tile',
            'duration': 500,
            },{
            'texture': 'purple-tile',
            'model': 'purple-tile',
            'duration': 500,
            },{
            'texture': 'green-tile',
            'model': 'green-tile',
            'duration': 500,
            },{
            'texture': 'blue-tile',
            'model': 'blue-tile',
            'duration': 500,
            }]
        animation_manager.load_animation('tile_animation', 4, frames)

    def setup_tile_map(self):
        map_manager = self.gameworld.managers["map_manager"]

        tiles = []
        for i in range(100):
            tiles_i = []
            for j in range(100):
                if randint(0,100) < 10:
                    tiles_i_j = [{'animation':'tile_animation', 'layer':0}]
                else:
                    tile_name = choice(['orange-tile', 'purple-tile', 'green-tile', 'blue-tile'])
                    tiles_i_j = [{'texture':tile_name,
                                 'model':tile_name,
                                 'layer':0}]
                tiles_i.append(tiles_i_j)
            tiles.append(tiles_i)

        map_manager.load_map('my_map', 100, 100, tiles)
        my_map = map_manager.maps['my_map']
        my_map.z_index_map = [0]
        my_map.tile_size = (64, 64)

        map_utils.init_entities_from_map(map_manager.maps['my_map'], self.gameworld.init_entity)

    def setup_states(self):
        self.gameworld.add_state(state_name='main',
                                 systems_added=['map_layer0'],
                                 systems_unpaused=['map_layer0','map_layer0_animator'])

    def set_state(self):
        self.gameworld.state = 'main'


class YourAppNameApp(App):
    pass


if __name__ == '__main__':
    YourAppNameApp().run()
