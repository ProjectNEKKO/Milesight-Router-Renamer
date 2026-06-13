import streamlit as st
import zipfile
import io

st.set_page_config(page_title="Router Screenshot Automator", page_icon="📸")

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

def reset_app():
    st.session_state.reset_counter += 1


NAMING_SEQUENCE = [
    "Overall Status",
    "Cellular",
    "Link Failover1",
    "Link Failover2",
    "APN 1",
    "APN 2",
    "WAN DNS",
    "WLAN",
    "DHCP",
    "ACS",
    "Port Mapping",
    "Custom Rule",
    "Auto Provision",
    "Device Management",
    "Milesight VPN",
    "Ping GCP Instance",
    "Ping Device Hub",
    "Ping Google",
    "Ping Youtube"

]
st.title("📸 Milesight Batch Renamer")
col1, col2 = st.columns(2)

with col1:
    router_prefix = st.text_input(
        "Router ID / Prefix:",
        placeholder="e.g., B2L21",
        help="This prefixes the individual image files.",
        key=f"prefix_{st.session_state.reset_counter}"
    )

with col2:
    custom_zip_name = st.text_input(
        "Custom ZIP Name (Optional):",
        placeholder="e.g., Site_A_Batch",
        help="Overrides the final downloaded ZIP filename.",
        key=f"zip_{st.session_state.reset_counter}"
    )

uploaded_files = st.file_uploader(
    "Drag & drop your screenshots here",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.reset_counter}"
)

if uploaded_files:
    uploaded_files = sorted(uploaded_files, key=lambda x: x.name)
    total_uploaded = len(uploaded_files)
    st.info(f"📁 Processed {total_uploaded} screenshots.")
    if total_uploaded > len(NAMING_SEQUENCE):
        st.warning(f"⚠️ You uploaded {total_uploaded} files, but the sequence only has {len(NAMING_SEQUENCE)}. Extras will be ignored.")
    elif total_uploaded < len(NAMING_SEQUENCE):
        st.warning(f"⚠️ You only uploaded {total_uploaded} files. The sequence expects {len(NAMING_SEQUENCE)}.")
    st.divider()
    zip_buffer = io.BytesIO()
    cols = st.columns(2)
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, file in enumerate(uploaded_files):
            if i < len(NAMING_SEQUENCE):
                prefix_str = f"{router_prefix}_" if router_prefix else ""
                base_name = NAMING_SEQUENCE[i]
                new_name = f"{prefix_str}{base_name}.png"
                file_bytes = file.getvalue()
                zip_file.writestr(new_name, file_bytes)
                with cols[i % 2]:
                    st.success(f"✅ {new_name}")


    st.divider()
    if custom_zip_name:
        download_name = custom_zip_name if custom_zip_name.lower().endswith('.zip') else f"{custom_zip_name}.zip"

    else:
        download_name = f"{router_prefix}_Configs.zip" if router_prefix else "Router_Configs.zip"

    btn_col1, btn_col2 = st.columns([3, 1])

    with btn_col1:
        st.download_button(
            label=f"📥 Download {download_name}",
            data=zip_buffer.getvalue(),
            file_name=download_name,
            mime="application/zip",
            use_container_width=True

        )

    with btn_col2:
        st.button(
            label="🔄 Reset App",
            on_click=reset_app,
            use_container_width=True
        )

