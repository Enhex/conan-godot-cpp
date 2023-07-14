#include <godot_cpp/classes/sprite2d.hpp>

namespace godot
{
	struct Test : Sprite2D
	{
		GDCLASS(Test, Sprite2D)

	protected:
		static void _bind_methods(){}
	};
}


int main()
{
}
