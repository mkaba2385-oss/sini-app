import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import useAuthStore from "../store/authStore.js";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

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

  function isActive(path) {
    if (path === "/") {
      return location.pathname === "/";
    }

    return location.pathname.startsWith(path);
  }

  const navLinks = [
    {
      label: "Accueil",
      path: "/",
    },
    {
      label: "Mes parcelles",
      path: "/parcelles",
    },
    {
      label: "Prix des marchés",
      path: "/prix",
    },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/95 backdrop-blur">
      <nav
        className="mx-auto flex min-h-18 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8"
        aria-label="Navigation principale"
      >
        {/* Logo */}
        <Link
          to="/"
          onClick={closeMenu}
          className="group flex items-center gap-2 rounded-xl px-2 py-1.5"
          aria-label="Sini - Accueil"
        >
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-50 text-xl transition-transform duration-200 group-hover:scale-105">
            🌱
          </span>

          <span className="text-2xl font-extrabold tracking-tight text-green-800">
            Sini
          </span>
        </Link>

        {accessToken ? (
          <>
            {/* Navigation desktop */}
            <div className="hidden items-center gap-1 md:flex">
              {navLinks.map((link) => {
                const active = isActive(link.path);

                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`rounded-xl px-4 py-2.5 text-sm font-semibold transition-all duration-200 ${
                      active
                        ? "bg-green-50 text-green-800 shadow-sm"
                        : "text-slate-600 hover:bg-slate-50 hover:text-green-800"
                    }`}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </div>

            {/* Compte desktop */}
            <div className="hidden items-center gap-3 md:flex">
              <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-green-700 text-sm font-bold text-white">
                  {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
                </div>

                <div className="hidden lg:block">
                  <p className="max-w-32 truncate text-sm font-semibold text-slate-800">
                    {user?.full_name || "Utilisateur"}
                  </p>

                  <p className="text-xs text-slate-500">Agriculteur</p>
                </div>
              </div>

              <button
                type="button"
                onClick={handleLogout}
                className="rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm font-semibold text-slate-600 transition-all duration-200 hover:border-red-200 hover:bg-red-50 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-red-200"
              >
                Déconnexion
              </button>
            </div>

            {/* Bouton mobile */}
            <button
              type="button"
              onClick={() => setMenuOpen((current) => !current)}
              className="flex h-11 w-11 items-center justify-center rounded-xl border border-slate-200 text-slate-700 transition-colors hover:bg-slate-50 md:hidden"
              aria-label={
                menuOpen ? "Fermer le menu" : "Ouvrir le menu"
              }
              aria-expanded={menuOpen}
            >
              <span className="text-xl leading-none">
                {menuOpen ? "×" : "☰"}
              </span>
            </button>
          </>
        ) : (
          <Link
            to="/login"
            className="rounded-xl bg-green-700 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-200 hover:bg-green-800 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-green-200"
          >
            Se connecter
          </Link>
        )}
      </nav>

      {/* Menu mobile */}
      {accessToken && menuOpen && (
        <div className="border-t border-slate-200 bg-white md:hidden">
          <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6">
            <div className="mb-4 flex items-center gap-3 rounded-2xl bg-slate-50 p-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-700 font-bold text-white">
                {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
              </div>

              <div className="min-w-0">
                <p className="truncate font-semibold text-slate-800">
                  {user?.full_name || "Utilisateur"}
                </p>

                <p className="text-sm text-slate-500">Agriculteur</p>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              {navLinks.map((link) => {
                const active = isActive(link.path);

                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={closeMenu}
                    className={`rounded-xl px-4 py-3.5 text-sm font-semibold transition-colors ${
                      active
                        ? "bg-green-50 text-green-800"
                        : "text-slate-600 hover:bg-slate-50 hover:text-green-800"
                    }`}
                  >
                    {link.label}
                  </Link>
                );
              })}

              <button
                type="button"
                onClick={handleLogout}
                className="mt-2 rounded-xl border border-red-100 bg-red-50 px-4 py-3.5 text-left text-sm font-semibold text-red-600 transition-colors hover:bg-red-100"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

export default Navbar;