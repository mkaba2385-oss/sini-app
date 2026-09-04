import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore.js";

function Navbar() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);
  const accessToken = useAuthStore((state) => state.accessToken);
  const logout = useAuthStore((state) => state.logout);

  const [menuOpen, setMenuOpen] = useState(false);

  function handleLogout() {
    logout();
    setMenuOpen(false);
    navigate("/login", { replace: true });
  }

  function closeMenu() {
    setMenuOpen(false);
  }

  return (
    <nav className="border-b bg-white shadow-sm">
      <div className="mx-auto max-w-6xl px-4 py-4 sm:px-6">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link
            to="/"
            onClick={closeMenu}
            className="shrink-0 text-xl font-bold text-green-800 sm:text-2xl"
          >
            Sini 🌱
          </Link>

          {accessToken && (
            <>
              {/* Menu desktop */}
              <div className="hidden items-center gap-4 md:flex">
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

                <Link
                  to="/prix"
                  className="font-medium text-gray-700 hover:text-green-700"
                >
                  Prix des marchés
                </Link>

                <span className="hidden text-sm text-gray-500 lg:block">
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

              {/* Bouton mobile */}
              <button
                type="button"
                onClick={() => setMenuOpen((current) => !current)}
                className="rounded-lg border border-gray-300 px-4 py-2 text-2xl text-gray-700 md:hidden"
                aria-label={
                  menuOpen
                    ? "Fermer le menu"
                    : "Ouvrir le menu"
                }
                aria-expanded={menuOpen}
              >
                {menuOpen ? "×" : "☰"}
              </button>
            </>
          )}

          {!accessToken && (
            <Link
              to="/login"
              className="rounded-lg bg-green-700 px-4 py-2 font-semibold text-white hover:bg-green-800"
            >
              Connexion
            </Link>
          )}
        </div>

        {/* Menu mobile */}
        {accessToken && menuOpen && (
          <div className="mt-4 border-t border-gray-200 pt-4 md:hidden">
            <div className="flex flex-col gap-2">
              <Link
                to="/"
                onClick={closeMenu}
                className="rounded-lg px-4 py-3 font-medium text-gray-700 hover:bg-green-50 hover:text-green-700"
              >
                Accueil
              </Link>

              <Link
                to="/parcelles"
                onClick={closeMenu}
                className="rounded-lg px-4 py-3 font-medium text-gray-700 hover:bg-green-50 hover:text-green-700"
              >
                Mes parcelles
              </Link>

              <Link
                to="/prix"
                onClick={closeMenu}
                className="rounded-lg px-4 py-3 font-medium text-gray-700 hover:bg-green-50 hover:text-green-700"
              >
                Prix des marchés
              </Link>

              {user?.full_name && (
                <div className="px-4 py-3 text-sm text-gray-500">
                  {user.full_name}
                </div>
              )}

              <button
                type="button"
                onClick={handleLogout}
                className="mt-2 rounded-lg bg-red-600 px-4 py-3 text-left font-semibold text-white hover:bg-red-700"
              >
                Déconnexion
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;