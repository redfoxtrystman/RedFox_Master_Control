namespace UnityEngine
{
    public class Object
    {
        public static void DontDestroyOnLoad(Object target) { }
    }

    public class Component : Object { }
    public class Behaviour : Component { }

    public class MonoBehaviour : Behaviour
    {
        protected MonoBehaviour() { }
    }

    public class GameObject : Object
    {
        public GameObject(string name) { }
        public T AddComponent<T>() where T : Component => default;
    }
}
