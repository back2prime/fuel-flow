import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

const FUEL_CORAL = "#FF385C";

function Avatar({ name, surname }) {
  const initials =
    `${name?.[0] ?? ""}${surname?.[0] ?? ""}`.toUpperCase() || "?";
  return (
    <div
      className="flex items-center justify-center rounded-full text-white font-semibold text-2xl select-none"
      style={{
        width: 80,
        height: 80,
        background: `linear-gradient(135deg, ${FUEL_CORAL} 0%, #ff6b35 100%)`,
        flexShrink: 0,
      }}
    >
      {initials}
    </div>
  );
}

function SectionCard({ title, children }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100">
        <h2 className="text-base font-semibold text-gray-900">{title}</h2>
      </div>
      <div className="px-6 py-5">{children}</div>
    </div>
  );
}

function Field({ label, name, type = "text", value, onChange, disabled }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
        {label}
      </label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        disabled={disabled}
        className="w-full rounded-xl border border-gray-200 px-4 py-2.5 text-sm text-gray-900 bg-gray-50 focus:outline-none focus:ring-2 focus:border-transparent transition disabled:opacity-50 disabled:cursor-not-allowed"
        style={{ "--tw-ring-color": FUEL_CORAL }}
      />
    </div>
  );
}

function StatusBadge({ type, message }) {
  if (!message) return null;
  const styles =
    type === "success"
      ? "bg-green-50 text-green-700 border-green-200"
      : "bg-red-50 text-red-600 border-red-200";
  return (
    <div className={`rounded-xl border px-4 py-2.5 text-sm ${styles}`}>
      {message}
    </div>
  );
}

export default function ProfilePage() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // profile edit
  const [profile, setProfile] = useState({
    name: "",
    surname: "",
    email: "",
    birth_date: "",
  });
  const [profileStatus, setProfileStatus] = useState(null); // {type, message}
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileDirty, setProfileDirty] = useState(false);

  // password
  const [pwd, setPwd] = useState({
    current_password: "",
    new_password: "",
    confirm: "",
  });
  const [pwdStatus, setPwdStatus] = useState(null);
  const [pwdSaving, setPwdSaving] = useState(false);

  // delete
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    api
      .get("/users/me")
      .then((res) => {
        setUser(res.data);
        setProfile({
          name: res.data.name ?? "",
          surname: res.data.surname ?? "",
          email: res.data.email ?? "",
          birth_date: res.data.birth_date ?? "",
        });
      })
      .catch(() => navigate("/login"))
      .finally(() => setLoading(false));
  }, [navigate]);

  const handleProfileChange = (e) => {
    setProfile((p) => ({ ...p, [e.target.name]: e.target.value }));
    setProfileDirty(true);
    setProfileStatus(null);
  };

  const handleProfileSave = async () => {
  setProfileSaving(true);
  setProfileStatus(null);
  try {
    const payload = {};
    if (profile.name !== user.name) payload.name = profile.name;
    if (profile.surname !== user.surname) payload.surname = profile.surname;
    if (profile.email !== user.email) payload.email = profile.email;
    if (profile.birth_date !== (user.birth_date ?? "")) payload.birth_date = profile.birth_date || null;

    if (Object.keys(payload).length === 0) {
      setProfileStatus({ type: "success", message: "Nothing to update." });
      setProfileDirty(false);
      return;
    }

    const res = await api.patch("/users/me", payload);
    setUser(res.data);
    setProfileDirty(false);
    setProfileStatus({ type: "success", message: "Profile updated." });
  } catch (e) {
    setProfileStatus({
      type: "error",
      message: e.response?.data?.detail ?? "Failed to save changes.",
    });
  } finally {
    setProfileSaving(false);
  }
};

  const handlePwdChange = (e) => {
    setPwd((p) => ({ ...p, [e.target.name]: e.target.value }));
    setPwdStatus(null);
  };

  const handlePwdSave = async () => {
    if (pwd.new_password !== pwd.confirm) {
      setPwdStatus({ type: "error", message: "New passwords don't match." });
      return;
    }
    if (pwd.new_password.length < 6) {
      setPwdStatus({
        type: "error",
        message: "New password must be at least 6 characters.",
      });
      return;
    }
    setPwdSaving(true);
    setPwdStatus(null);
    try {
      await api.patch("/users/me/password", {
        current_password: pwd.current_password,
        new_password: pwd.new_password,
      });
      setPwd({ current_password: "", new_password: "", confirm: "" });
      setPwdStatus({ type: "success", message: "Password changed." });
    } catch (e) {
      setPwdStatus({
        type: "error",
        message: e.response?.data?.detail ?? "Failed to change password.",
      });
    } finally {
      setPwdSaving(false);
    }
  };

  const handleDelete = async () => {
    setDeleteLoading(true);
    setDeleteError(null);
    try {
      await api.delete("/users/me");
      localStorage.removeItem("access_token");
      navigate("/");
    } catch (e) {
      setDeleteError(e.response?.data?.detail ?? "Failed to delete account.");
      setDeleteLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div
          className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin"
          style={{ borderColor: `${FUEL_CORAL} transparent transparent transparent` }}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-10 flex flex-col gap-6">

        {/* Header */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-6 flex items-center gap-5">
          <Avatar name={user?.name} surname={user?.surname} />
          <div className="flex flex-col gap-0.5">
            <h1 className="text-xl font-bold text-gray-900">
              {user?.name} {user?.surname}
            </h1>
            <span className="text-sm text-gray-400">@{user?.login}</span>
            <span className="text-sm text-gray-500 mt-0.5">{user?.email}</span>
          </div>
        </div>

        {/* Edit Profile */}
        <SectionCard title="Personal information">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Field
              label="First name"
              name="name"
              value={profile.name}
              onChange={handleProfileChange}
            />
            <Field
              label="Last name"
              name="surname"
              value={profile.surname}
              onChange={handleProfileChange}
            />
            <Field
              label="Email"
              name="email"
              type="email"
              value={profile.email}
              onChange={handleProfileChange}
            />
            <Field
              label="Date of birth"
              name="birth_date"
              type="date"
              value={profile.birth_date}
              onChange={handleProfileChange}
            />
          </div>
          <div className="mt-5 flex items-center gap-3">
            <button
              onClick={handleProfileSave}
              disabled={profileSaving || !profileDirty}
              className="px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition disabled:opacity-40 disabled:cursor-not-allowed"
              style={{ background: FUEL_CORAL }}
            >
              {profileSaving ? "Saving…" : "Save changes"}
            </button>
            {profileStatus && (
              <StatusBadge
                type={profileStatus.type}
                message={profileStatus.message}
              />
            )}
          </div>
        </SectionCard>

        {/* Change Password */}
        <SectionCard title="Change password">
          <div className="flex flex-col gap-4">
            <Field
              label="Current password"
              name="current_password"
              type="password"
              value={pwd.current_password}
              onChange={handlePwdChange}
            />
            <Field
              label="New password"
              name="new_password"
              type="password"
              value={pwd.new_password}
              onChange={handlePwdChange}
            />
            <Field
              label="Confirm new password"
              name="confirm"
              type="password"
              value={pwd.confirm}
              onChange={handlePwdChange}
            />
          </div>
          <div className="mt-5 flex items-center gap-3">
            <button
              onClick={handlePwdSave}
              disabled={
                pwdSaving ||
                !pwd.current_password ||
                !pwd.new_password ||
                !pwd.confirm
              }
              className="px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition disabled:opacity-40 disabled:cursor-not-allowed"
              style={{ background: FUEL_CORAL }}
            >
              {pwdSaving ? "Saving…" : "Update password"}
            </button>
            {pwdStatus && (
              <StatusBadge type={pwdStatus.type} message={pwdStatus.message} />
            )}
          </div>
        </SectionCard>

        {/* Danger Zone */}
        <SectionCard title="Danger zone">
          <p className="text-sm text-gray-500 mb-4">
            Permanently delete your account and all associated data. This action
            cannot be undone.
          </p>
          <button
            onClick={() => setShowDeleteModal(true)}
            className="px-5 py-2.5 rounded-xl text-sm font-semibold border transition"
            style={{ color: FUEL_CORAL, borderColor: FUEL_CORAL }}
          >
            Delete account
          </button>
        </SectionCard>
      </div>

      {/* Delete confirm modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 flex flex-col gap-4">
            <h3 className="text-lg font-bold text-gray-900">Delete account?</h3>
            <p className="text-sm text-gray-500">
              This will permanently delete <strong>@{user?.login}</strong> and
              all your favourites. You can't undo this.
            </p>
            {deleteError && (
              <StatusBadge type="error" message={deleteError} />
            )}
            <div className="flex gap-3 justify-end mt-1">
              <button
                onClick={() => {
                  setShowDeleteModal(false);
                  setDeleteError(null);
                }}
                disabled={deleteLoading}
                className="px-4 py-2 rounded-xl text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={deleteLoading}
                className="px-4 py-2 rounded-xl text-sm font-semibold text-white transition disabled:opacity-50"
                style={{ background: FUEL_CORAL }}
              >
                {deleteLoading ? "Deleting…" : "Yes, delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
