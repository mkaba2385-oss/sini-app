import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore.js";

function Navbar() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);
  const accessToken = useAuthStore((state) => state.accessToken);
  const logout = useAuthStore((state) => state.logout);

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <nav className="border-b bg-white shadow-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link
          to="/"
          className="text-xl font-bold text-green-800"
        >
          Sini 🌱
        </Link>

        {accessToken ? (
          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="font-medium text-gray-700 hover:text-green-700"
            >
              Accueil
            </Link>

            <Link
              to="/parcelles"
              className="font-medium text-gray-700 hover:text-green-700"
            >
              Mes parcelles
            </Link>

            <span className="hidden text-sm text-gray-500 md:block">
              {user?.full_name || ""}
            </span>

            <button
              type="button"
              onClick={handleLogout}
              className="rounded-lg bg-red-600 px-4 py-2 font-semibold text-white hover:bg-red-700"
            >
              Déconnexion
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            className="rounded-lg bg-green-700 px-4 py-2 font-semibold text-white hover:bg-green-800"
          >
            Connexion
          </Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;