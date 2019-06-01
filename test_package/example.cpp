#include <Godot.hpp>
#include <Node.hpp>

namespace godot
{
	struct Test : Node
	{
		GODOT_CLASS(Test, Node)

	public:
		static void _register_methods(){}
		void _init(){}
	};
}


int main()
{
}
