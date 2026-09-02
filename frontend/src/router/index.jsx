import { BrowserRouter, Route, Routes } from "react-router-dom";

import AddJournalEntryPage from "../pages/AddJournalEntryPage.jsx";
import AddParcellePage from "../pages/AddParcellePage.jsx";
import EditJournalEntryPage from "../pages/EditJournalEntryPage.jsx";
import EditParcellePage from "../pages/EditParcellePage.jsx";
import HomePage from "../pages/HomePage.jsx";
import JournalPage from "../pages/JournalPage.jsx";
import LoginOtpPage from "../pages/LoginOtpPage.jsx";
import LoginPage from "../pages/LoginPage.jsx";
import OtpPage from "../pages/OtpPage.jsx";
import ParcellesPage from "../pages/ParcellesPage.jsx";
import RegisterPage from "../pages/RegisterPage.jsx";
import ProtectedRoute from "./ProtectedRoute.jsx";

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ==================== ROUTES PUBLIQUES ==================== */}

        <Route path="/login" element={<LoginPage />} />

        <Route
          path="/verify-login-otp"
          element={<LoginOtpPage />}
        />

        <Route
          path="/verify-otp"
          element={<OtpPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />

        {/* ==================== ROUTES PROTÉGÉES ==================== */}

        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<HomePage />} />

          <Route
            path="/parcelles"
            element={<ParcellesPage />}
          />

          <Route
            path="/parcelles/new"
            element={<AddParcellePage />}
          />

          <Route
            path="/parcelles/:id/edit"
            element={<EditParcellePage />}
          />

          <Route
            path="/parcelles/:parcelleId/journal"
            element={<JournalPage />}
          />

          <Route
            path="/journal/new"
            element={<AddJournalEntryPage />}
          />

          <Route
            path="/journal/:entryId/edit"
            element={<EditJournalEntryPage />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;