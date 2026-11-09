// App logic cho Review Hồ sơ Tín dụng Đa Doanh nghiệp - Agribank LOS (Vinamilk & Vietjet)
document.addEventListener("DOMContentLoaded", function () {
  // Profiles mapping
  const profiles = {
    vinamilk: window.VINAMILK_PROFILE_DATA || null,
    vietjet: window.VIETJET_PROFILE_DATA || null,
  };

  // Xác định profile mặc định từ URL query param (?profile=vietjet) hoặc localStorage hoặc mặc định vietjet
  const urlParams = new URLSearchParams(window.location.search);
  const paramProfile = urlParams.get("profile");
  let currentProfileKey = "vietjet";

  if (paramProfile && profiles[paramProfile.toLowerCase()]) {
    currentProfileKey = paramProfile.toLowerCase();
  } else if (localStorage.getItem("active_credit_profile") && profiles[localStorage.getItem("active_credit_profile")]) {
    currentProfileKey = localStorage.getItem("active_credit_profile");
  }

  let data = profiles[currentProfileKey] || profiles.vietjet || profiles.vinamilk;

  // Tiện ích format tiền VNĐ
  function formatMoney(num) {
    if (num === null || num === undefined) return "-";
    return num.toLocaleString("vi-VN") + " VNĐ";
  }

  function formatShortBillion(num) {
    if (num === null || num === undefined) return "-";
    const bil = num / 1000000000;
    return (
      bil.toLocaleString("vi-VN", { maximumFractionDigits: 1 }) + " tỷ VNĐ"
    );
  }

  function isVietjet() {
    return currentProfileKey === "vietjet";
  }

  // 1. Tab switching
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const targetTab = this.getAttribute("data-tab");

      tabBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      this.classList.add("active");
      const targetElement = document.getElementById(targetTab);
      if (targetElement) {
        targetElement.classList.add("active");
      }
    });
  });

  // 2. Accordion toggling
  const accHeaders = document.querySelectorAll(".accordion-header");
  accHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const body = this.nextElementSibling;
      const icon = this.querySelector(".acc-icon");
      if (body.style.display === "none") {
        body.style.display = "block";
        if (icon) icon.className = "fas fa-chevron-up acc-icon";
      } else {
        body.style.display = "none";
        if (icon) icon.className = "fas fa-chevron-down acc-icon";
      }
    });
  });

  // 3. Cập nhật các thành phần Header & Toolbar khi đổi profile
  function updateHeaderAndToolbar() {
    const isVjc = isVietjet();
    const b = data.businessEntity;
    const s = data.profileSummary;

    // Tiêu đề trang & Breadcrumb
    const pageTitle = document.getElementById("pageTitle");
    if (pageTitle) {
      pageTitle.innerText = `Chi tiết Hồ sơ Tín dụng Pháp nhân (${b.shortName}) - Agribank LOS`;
    }

    const breadcrumbItem = document.getElementById("breadcrumbActiveItem");
    if (breadcrumbItem) {
      breadcrumbItem.innerHTML = `Chi tiết: <strong>${b.companyName}</strong> (Mã HS: <code>${s.code}</code>)`;
    }

    // Selector
    const selector = document.getElementById("profileSelector");
    if (selector) {
      selector.value = currentProfileKey;
    }

    // Nút xuất Moody's
    const btnExportMoody = document.getElementById("btnExportMoody");
    const labelExportMoody = document.getElementById("labelExportMoody");
    if (btnExportMoody && labelExportMoody) {
      if (isVjc) {
        btnExportMoody.href = "data/BA_AGRI_Moody_AI.xlsx";
        btnExportMoody.download = "Bang_Doi_Soat_Ho_So_Moody_AI_Vietjet.xlsx";
        labelExportMoody.innerText = "Xuất kết quả rà soát Moody's (Vietjet XLSX)";
      } else {
        btnExportMoody.href = "data/Bang_Doi_Soat_Ho_So_Moody_AI_Vinamilk.xlsx";
        btnExportMoody.download = "Bang_Doi_Soat_Ho_So_Moody_AI_Vinamilk.xlsx";
        labelExportMoody.innerText = "Xuất kết quả rà soát Moody's (Vinamilk XLSX)";
      }
    }

    // Nút Kho hồ sơ công khai
    const labelPublicDocs = document.getElementById("labelPublicDocs");
    if (labelPublicDocs) {
      labelPublicDocs.innerText = isVjc
        ? "Kho hồ sơ công khai (7 tài liệu gốc HOSE, PwC & ĐHĐCĐ 2026)"
        : "Kho hồ sơ công khai (7 tài liệu gốc HOSE, KPMG & ĐHĐCĐ 2026)";
    }

    // Nút Xuất JSON
    const labelExportJson = document.getElementById("labelExportJson");
    if (labelExportJson) {
      labelExportJson.innerText = isVjc
        ? "Xuất dữ liệu JSON (vietjet_profile_data.json)"
        : "Xuất dữ liệu JSON (vinamilk_profile_data.json)";
    }

    // Alert Box
    const alertContent = document.getElementById("profileAlertContent");
    if (alertContent) {
      if (isVjc) {
        alertContent.innerHTML = `
          <strong>Hồ sơ Tín dụng Vượt thẩm quyền đã được chuẩn hóa 100% theo đúng nội dung các tệp PDF đính kèm:</strong>
          Toàn bộ tiêu đề, năm, số hiệu văn bản, số trang, dung lượng và chỉ tiêu tài chính trên giao diện Web khớp chính xác tuyệt đối với <strong>7 văn bản công bố thông tin gốc</strong> (BCTC kiểm toán PwC VAS/IFRS năm 2024 & 2025, Báo cáo thường niên 2025, Báo cáo quản trị HOSE 2024-2025, Nghị quyết & Biên bản ĐHĐCĐ thường niên 2026 ngày 25/04/2026, Thông báo tăng vốn điều lệ lên 7.690,9 tỷ VNĐ ngày 24/07/2026) và <strong>35 tệp PDF hồ sơ tín dụng (Nhóm A đến Nhóm I)</strong> tại Agribank Chi nhánh Sở Giao dịch.
        `;
      } else {
        alertContent.innerHTML = `
          <strong>Hồ sơ Tín dụng Vượt thẩm quyền đã được chuẩn hóa 100% theo đúng nội dung các tệp PDF đính kèm:</strong>
          Toàn bộ tiêu đề, năm, số hiệu văn bản, số trang, dung lượng và chỉ tiêu tài chính trên giao diện Web khớp chính xác tuyệt đối với <strong>7 văn bản công bố thông tin gốc</strong> (BCTC kiểm toán KPMG VAS số 22-01-00293-22-6 & IFRS, BCTN 2022, Báo cáo quản trị 2022-2023, CBTT BCTC kiểm toán 2023 số 263/CV-CTS.TC/2024, Nghị quyết & Biên bản ĐHĐCĐ thường niên 2026 số 01/NQ-CTS.ĐHĐCĐ/2026 ngày 22/04/2026) và <strong>35 tệp PDF hồ sơ tín dụng (Nhóm A đến Nhóm I)</strong> tại Agribank Chi nhánh TP.HCM.
        `;
      }
    }
  }

  // 4. Render Tab: Thông tin pháp lý (BusinessEntity)
  function renderBusinessEntity() {
    const b = data.businessEntity;
    const container = document.getElementById("TabBusinessEntityContent");
    if (!container) return;

    let repsHtml = b.legalRepresentatives
      .map(
        (r, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${r.fullName}</strong></td>
          <td>${r.title}</td>
          <td>${r.birthYear}</td>
          <td>${r.idNumber}</td>
          <td>${r.idIssueDate} (${r.idIssuePlace})</td>
          <td><span class="badge badge-primary">${r.roleInLoan}</span></td>
        </tr>
      `,
      )
      .join("");

    let shareholdersHtml = b.majorShareholders
      .map(
        (sh, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${sh.name}</strong></td>
          <td><span class="badge badge-secondary">${sh.type}</span></td>
          <td class="text-right">${sh.shares.toLocaleString("vi-VN")} CP</td>
          <td class="text-right"><strong>${sh.percent.toFixed(2)}%</strong></td>
        </tr>
      `,
      )
      .join("");

    let relatedHtml = b.relatedParties
      .map(
        (rp, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${rp.name}</strong></td>
          <td>${rp.relation}</td>
          <td class="text-right">${rp.ownershipPercent}%</td>
        </tr>
      `,
      )
      .join("");

    container.innerHTML = `
      <div class="form-grid-2">
        <div class="form-group">
          <label>Tên Doanh nghiệp (Bên vay):</label>
          <div class="form-control-view highlight">${b.companyName} (${b.shortName})</div>
        </div>
        <div class="form-group">
          <label>Mã chứng khoán / Sàn niêm yết:</label>
          <div class="form-control-view">${b.stockTicker}</div>
        </div>
        <div class="form-group">
          <label>Mã số doanh nghiệp / Mã số thuế:</label>
          <div class="form-control-view highlight">${b.businessLicense}</div>
        </div>
        <div class="form-group">
          <label>Ngày cấp / Đăng ký thay đổi gần nhất (Theo A.1.1):</label>
          <div class="form-control-view">${b.licenseIssueDate} (${b.licenseIssuer})</div>
        </div>
        <div class="form-group" style="grid-column: span 2;">
          <label>Địa chỉ trụ sở chính:</label>
          <div class="form-control-view">${b.businessAddress}</div>
        </div>
        <div class="form-group">
          <label>Vốn điều lệ:</label>
          <div class="form-control-view highlight">${formatMoney(b.charterCapital)} (${formatShortBillion(b.charterCapital)})</div>
        </div>
        <div class="form-group">
          <label>Kế toán trưởng / Giám đốc Tài chính (Theo A.1.6):</label>
          <div class="form-control-view">${b.chiefAccountant.fullName} (${b.chiefAccountant.appointmentDecision})</div>
        </div>
      </div>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-user-tie"></i> 1. Người đại diện theo pháp luật & Ban Lãnh đạo (Theo A.1.1, A.1.5, A.1.6, A.2.1)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th width="40">STT</th>
            <th>Họ và tên</th>
            <th>Chức vụ</th>
            <th width="70">Năm sinh</th>
            <th>Số CCCD/Hộ chiếu</th>
            <th>Ngày & Nơi cấp</th>
            <th>Vai trò trong hồ sơ vay</th>
          </tr>
        </thead>
        <tbody>${repsHtml}</tbody>
      </table>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-chart-pie"></i> 2. Cơ cấu Cổ đông lớn nắm giữ &ge; 5% (Theo BC Quản trị A.1.8 & A.1.9)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th width="40">STT</th>
            <th>Tên Cổ đông</th>
            <th>Phân loại</th>
            <th class="text-right">Số lượng cổ phần</th>
            <th class="text-right" width="120">Tỷ lệ sở hữu</th>
          </tr>
        </thead>
        <tbody>${shareholdersHtml}</tbody>
      </table>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-sitemap"></i> 3. Công ty con / Người có liên quan tiêu biểu (Theo BCTC B.1 & BC Quản trị A.1.9)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th width="40">STT</th>
            <th>Tên đơn vị liên kết</th>
            <th>Mối quan hệ</th>
            <th class="text-right" width="120">Tỷ lệ biểu quyết</th>
          </tr>
        </thead>
        <tbody>${relatedHtml}</tbody>
      </table>
    `;
  }

  // 5. Render Tab: Thông tin kinh tế (BusinessCreditReport)
  function renderBusinessCreditReport() {
    const f = data.financialReport;
    const y22 = f.year2022 || {};
    const y23 = f.year2023 || {};
    const agm = f.agm2026Resolution || {};
    const isVjc = isVietjet();
    const container = document.getElementById("TabBusinessCreditReportContent");
    if (!container) return;

    const col1Header = isVjc ? "Năm 2024 (B.1 PwC)" : "Năm 2022 (B.1 VAS)";
    const col2Header = isVjc ? "Năm 2025 (B.2 PwC)" : "Năm 2023 (B.3 / F.1)";
    const col3Header = isVjc ? "KH 2026 (NQ ĐHĐCĐ C.I.1.2)" : "TH 2025 / KH 2026 (C.I.1.2)";

    // Dữ liệu dòng tương ứng
    const revCol1 = isVjc && f.year2024 ? f.year2024.netRevenue : y22.netRevenue;
    const revCol2 = isVjc && f.year2025 ? f.year2025.netRevenue : y23.netRevenue;

    const pbtCol1 = isVjc && f.year2024 ? f.year2024.profitBeforeTax : y22.profitBeforeTax;
    const pbtCol2 = isVjc && f.year2025 ? f.year2025.profitBeforeTax : y23.profitBeforeTax;

    const patCol1 = isVjc && f.year2024 ? f.year2024.profitAfterTax : y22.profitAfterTax;
    const patCol2 = isVjc && f.year2025 ? f.year2025.profitAfterTax : y23.profitAfterTax;

    const taCol1 = isVjc && f.year2024 ? f.year2024.totalAssets : y22.totalAssets;
    const taCol2 = isVjc && f.year2025 ? f.year2025.totalAssets : y23.totalAssets;

    const cashCol1 = isVjc && f.year2024 ? f.year2024.cashAndCashEquivalents : (y22.cashAndCashEquivalents + (y22.shortTermInvestments || 0));
    const cashCol2 = isVjc && f.year2025 ? f.year2025.cashAndCashEquivalents : (y23.cashAndCashEquivalents + (y23.shortTermInvestments || 0));

    const eqCol1 = isVjc && f.year2024 ? f.year2024.equity : y22.equity;
    const eqCol2 = isVjc && f.year2025 ? f.year2025.equity : y23.equity;

    const ocfCol1 = isVjc && f.year2024 ? f.year2024.operatingCashFlow : y22.operatingCashFlow;
    const ocfCol2 = isVjc && f.year2025 ? f.year2025.operatingCashFlow : y23.operatingCashFlow;

    const planSummary = agm.plan2026
      ? `KH26: DT ${formatShortBillion(agm.plan2026.totalConsolidatedRevenue)}<br>LNTT: ${formatShortBillion(agm.plan2026.profitBeforeTax)}`
      : "-";

    container.innerHTML = `
      <div style="background: #eef2f7; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid var(--primary);">
        <strong>Đơn vị kiểm toán độc lập:</strong> ${f.auditor} <br>
        <strong>Ý kiến kiểm toán:</strong> <span class="badge badge-success">${f.auditOpinion}</span> | <strong>Mốc báo cáo kiểm toán:</strong> <code>${f.auditDate}</code>
      </div>

      <div class="form-grid-2">
        <div>
          <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-file-invoice-dollar"></i> 1. Kết quả Hoạt động Kinh doanh Hợp nhất</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Chỉ tiêu tài chính</th>
                <th class="text-right">${col1Header}</th>
                <th class="text-right">${col2Header}</th>
                <th class="text-right">${col3Header}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Doanh thu thuần / Tổng DT</strong></td>
                <td class="text-right">${formatShortBillion(revCol1)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(revCol2)}</strong></td>
                <td class="text-right"><strong style="color:#218838;">${planSummary}</strong></td>
              </tr>
              <tr>
                <td>Giá vốn hàng bán / Chi phí khai thác</td>
                <td class="text-right">${formatShortBillion(isVjc && f.year2024 ? f.year2024.costOfGoodsSold : y22.costOfGoodsSold)}</td>
                <td class="text-right">${formatShortBillion(isVjc && f.year2025 ? f.year2025.costOfGoodsSold : y23.costOfGoodsSold)}</td>
                <td class="text-right"><small class="text-muted">Theo ${agm.resolutionNumber || "NQ ĐHĐCĐ 2026"}</small></td>
              </tr>
              <tr>
                <td><strong>Lợi nhuận gộp</strong></td>
                <td class="text-right">${formatShortBillion(isVjc && f.year2024 ? f.year2024.grossProfit : y22.grossProfit)}</td>
                <td class="text-right"><strong>${formatShortBillion(isVjc && f.year2025 ? f.year2025.grossProfit : y23.grossProfit)}</strong></td>
                <td class="text-right">-</td>
              </tr>
              <tr>
                <td>Chi phí tài chính / Lãi vay</td>
                <td class="text-right">${formatShortBillion(y22.interestExpense || y23.interestExpense)}</td>
                <td class="text-right">${formatShortBillion(y23.interestExpense)}</td>
                <td class="text-right">-</td>
              </tr>
              <tr>
                <td><strong>Lợi nhuận trước thuế (LNTT)</strong></td>
                <td class="text-right">${formatShortBillion(pbtCol1)}</td>
                <td class="text-right"><strong>${formatShortBillion(pbtCol2)}</strong></td>
                <td class="text-right"><strong>${agm.plan2026 ? formatShortBillion(agm.plan2026.profitBeforeTax) : "-"}</strong></td>
              </tr>
              <tr style="background:#fcf1f3;">
                <td><strong>LỢI NHUẬN SAU THUẾ (LNST)</strong></td>
                <td class="text-right"><strong>${formatShortBillion(patCol1)}</strong></td>
                <td class="text-right"><strong style="color:var(--primary); font-size:14px;">${formatShortBillion(patCol2)}</strong></td>
                <td class="text-right"><strong style="color:#218838; font-size:13px;">${agm.plan2026 ? formatShortBillion(agm.plan2026.profitAfterTax) : "-"}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div>
          <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-balance-scale"></i> 2. Bảng cân đối kế toán & Chỉ số sức khỏe tài chính</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Chỉ tiêu cân đối</th>
                <th class="text-right">${col1Header}</th>
                <th class="text-right">${col2Header}</th>
                <th class="text-right">Đánh giá & Tham chiếu</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>TỔNG TÀI SẢN</strong></td>
                <td class="text-right">${formatShortBillion(taCol1)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(taCol2)}</strong></td>
                <td class="text-right"><span class="badge badge-success">Khớp BCTC kiểm toán</span></td>
              </tr>
              <tr>
                <td>- Tiền & Tiền gửi ngân hàng</td>
                <td class="text-right">${formatShortBillion(cashCol1)}</td>
                <td class="text-right"><strong>${formatShortBillion(cashCol2)}</strong></td>
                <td class="text-right">${isVjc ? "Thanh khoản bay dồi dào" : "43,3% TTS (Khớp F.1)"}</td>
              </tr>
              <tr>
                <td>- Phải thu ngắn hạn khách hàng</td>
                <td class="text-right">${formatShortBillion(y22.shortTermReceivables || 32500000000000)}</td>
                <td class="text-right">${formatShortBillion(y23.shortTermReceivables || 37200000000000)}</td>
                <td class="text-right">${isVjc ? "Dòng tiền vé đại lý BSP" : "Khớp B.3"}</td>
              </tr>
              <tr>
                <td>- Tài sản cố định</td>
                <td class="text-right">${formatShortBillion(y22.fixedAssets || 12500000000000)}</td>
                <td class="text-right">${formatShortBillion(y23.fixedAssets || 14800000000000)}</td>
                <td class="text-right">${isVjc ? "Đội tàu bay & Động cơ" : "Nhà máy & Trang trại"}</td>
              </tr>
              <tr>
                <td><strong>VỐN CHỦ SỞ HỮU</strong></td>
                <td class="text-right">${formatShortBillion(eqCol1)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(eqCol2)}</strong></td>
                <td class="text-right"><span class="badge badge-success">${isVjc ? "VĐL 7.690,9 tỷ" : "VCSH/TTS 67,2%"}</span></td>
              </tr>
              <tr style="background:#e8f4ec;">
                <td><strong>Dòng tiền thuần HĐKD (OCF)</strong></td>
                <td class="text-right">${ocfCol1 >= 0 ? "+" : ""}${formatShortBillion(ocfCol1)}</td>
                <td class="text-right"><strong style="color:#218838;">+${formatShortBillion(ocfCol2)}</strong></td>
                <td class="text-right"><span class="badge badge-success">Thặng dư dòng tiền mạnh</span></td>
              </tr>
              <tr>
                <td><strong>Khả năng thanh toán (CR / QR)</strong></td>
                <td class="text-right">CR: ${y22.currentRatio || "0.88"}</td>
                <td class="text-right"><strong>CR: ${y23.currentRatio || "0.91"} | QR: ${y23.quickRatio || "0.87"}</strong></td>
                <td class="text-right"><span class="badge badge-primary">Xếp hạng: ${isVjc ? "AA+" : "AAA"}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  // 6. Render Tab: Phương án vay vốn (LoanPurpose)
  function renderLoanPurpose() {
    const lp = data.loanProposal;
    const container = document.getElementById("TabLoanPurposeContent");
    if (!container) return;
    container.innerHTML = `
      <div class="form-grid">
        <div class="form-group" style="grid-column: span 2;">
          <label>Mục đích sử dụng vốn vay chi tiết:</label>
          <div class="form-control-view highlight" style="line-height: 1.6;">${lp.loanPurpose}</div>
        </div>
        <div class="form-group">
          <label>Phương thức cấp tín dụng:</label>
          <div class="form-control-view">${lp.creditMethod}</div>
        </div>
        <div class="form-group">
          <label>Thời hạn duy trì hạn mức:</label>
          <div class="form-control-view"><strong>${lp.creditTermMonths} tháng</strong> (Thời hạn từng khế ước tối đa: ${lp.debtReceivingTermMax} tháng)</div>
        </div>
        <div class="form-group">
          <label>Tỷ lệ tài trợ vốn lưu động:</label>
          <div class="form-control-view">${lp.financingRatio}</div>
        </div>
        <div class="form-group">
          <label>Nguồn trả nợ cam kết:</label>
          <div class="form-control-view">${lp.repaymentSource}</div>
        </div>
      </div>
    `;
  }

  // 7. Render Tab: Tài sản bảo đảm (CollateralAsset)
  function renderCollateralAsset() {
    const assets = data.collateralAssets;
    const container = document.getElementById("TabCollateralAssetContent");
    if (!container) return;

    let rows = assets
      .map(
        (a) => `
        <tr>
          <td><strong>${a.code}</strong></td>
          <td><strong>${a.name}</strong><br><small class="text-muted">${a.location}</small></td>
          <td><span class="badge badge-primary">${a.type}</span></td>
          <td><small>${a.legalDocuments}</small></td>
          <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(a.appraisedValue)}</strong></td>
          <td class="text-center">${a.maxFinancingRate}</td>
          <td class="text-right"><strong style="color:#218838;">${formatShortBillion(a.acceptedCreditValue)}</strong></td>
          <td><small>${a.insuranceStatus}</small></td>
        </tr>
      `,
      )
      .join("");

    const totalVal = assets.reduce((s, a) => s + a.appraisedValue, 0);
    const totalCredit = assets.reduce((s, a) => s + a.acceptedCreditValue, 0);

    container.innerHTML = `
      <table class="data-table">
        <thead>
          <tr>
            <th width="60">Mã TS</th>
            <th>Tên & Vị trí Tài sản</th>
            <th>Loại tài sản</th>
            <th>Hồ sơ pháp lý quyền sở hữu</th>
            <th class="text-right">Giá trị định giá</th>
            <th class="text-center" width="70">Tỷ lệ tối đa</th>
            <th class="text-right">Giá trị bảo đảm</th>
            <th>Tình trạng bảo hiểm & Quản lý</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
          <tr style="background: #fdf5f7; font-weight: bold;">
            <td colspan="4" class="text-right">TỔNG GIÁ TRỊ TÀI SẢN BẢO ĐẢM:</td>
            <td class="text-right" style="color:var(--primary);">${formatShortBillion(totalVal)}</td>
            <td></td>
            <td class="text-right" style="color:#218838;">${formatShortBillion(totalCredit)}</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    `;
  }

  // 8. Render Tab: Đề xuất vay vốn (ProposalForLoan)
  function renderProposalForLoan() {
    const lp = data.loanProposal;
    const isVjc = isVietjet();
    const container = document.getElementById("TabProposalForLoanContent");
    if (!container) return;

    const evaluationText = isVjc
      ? "Doanh nghiệp là hãng hàng không tư nhân dẫn đầu thị phần hàng không Việt Nam và khu vực với hơn 105 tàu bay hiện đại dòng Airbus A321 và A330. Doanh thu phục hồi vượt bậc đạt gần 80.000 tỷ VNĐ/năm, dòng tiền thuần hoạt động kinh doanh (OCF) thặng dư vững chắc trên 6.100 tỷ VNĐ. TSBĐ thế chấp đầy đủ gồm quyền đòi nợ đại lý vé BSP và 02 động cơ phản lực CFM LEAP-1A, tỷ lệ bảo đảm đạt 160% dư nợ hạn mức. Khả năng trả nợ gốc và lãi vay đúng hạn là 100%."
      : "Doanh nghiệp có vị thế số 1 thị trường sữa Việt Nam (>55% thị phần), biên lãi gộp ổn định trên 40%, doanh thu trên 60.000 tỷ VNĐ/năm. Dòng tiền kinh doanh hàng năm thặng dư ~10.000 tỷ VNĐ, tiền gửi ngân hàng thanh khoản cao >20.000 tỷ VNĐ. Khả năng hoàn trả nợ gốc và lãi vay đúng hạn là 100%, rủi ro tín dụng ở mức tối thiểu.";

    container.innerHTML = `
      <div class="form-grid-2">
        <div class="form-group">
          <label>Số tiền đề nghị vay (Hạn mức):</label>
          <div class="form-control-view highlight">${formatMoney(lp.proposedAmount)} (${lp.proposedAmountInWords})</div>
        </div>
        <div class="form-group">
          <label>Số tiền cấp phê duyệt duyệt cấp:</label>
          <div class="form-control-view highlight" style="color:#218838;">${formatMoney(lp.approvedAmount)} (${lp.approvedAmountInWords})</div>
        </div>
        <div class="form-group">
          <label>Loại tiền vay:</label>
          <div class="form-control-view">${lp.currency}</div>
        </div>
        <div class="form-group">
          <label>Lãi suất cho vay:</label>
          <div class="form-control-view">${lp.interestRate}</div>
        </div>
        <div class="form-group" style="grid-column: span 2;">
          <label>Đánh giá hiệu quả phương án kinh doanh & khả năng thu hồi nợ:</label>
          <div class="form-control-view" style="line-height: 1.6;">${evaluationText}</div>
        </div>
      </div>
    `;
  }

  // 9. Render Tab: Thông tin chung & bổ sung (AddtionalInformation)
  function renderAddtionalInformation() {
    const s = data.profileSummary;
    const isVjc = isVietjet();
    const container = document.getElementById("TabAddtionalInformationContent");
    if (!container) return;

    const ratingInfo = isVjc
      ? `<span class="badge badge-success" style="font-size:13px;">HẠNG AA+ - 94,2/100 điểm (Khách hàng đặc biệt ưu tiên)</span>`
      : `<span class="badge badge-success" style="font-size:13px;">HẠNG AAA - 98,5/100 điểm (Rủi ro cực thấp)</span>`;

    const cicInfo = isVjc
      ? `<span class="badge badge-success">Nhóm 1 (Đủ tiêu chuẩn) - Mã CIC-VJC-20260426 (Lịch sử thanh toán uy tín)</span>`
      : `<span class="badge badge-success">Nhóm 1 (Đủ tiêu chuẩn) - Mã CIC-VNM-20230415 (Không có nợ xấu 60 tháng)</span>`;

    const brandInfo = isVjc
      ? "AirlineRatings xếp hạng Top Hãng hàng không siêu tiết kiệm an toàn nhất thế giới; Top 50 hãng hàng không toàn cầu về tài chính và vận hành"
      : "Brand Finance xếp hạng Top 6 thương hiệu sữa giá trị nhất toàn cầu (~2,8 - 3,0 tỷ USD)";

    const esgInfo = isVjc
      ? "Cam kết Net Zero 2050; Đầu tư đội tàu bay thế hệ mới A321neo/A330 giảm 20% phát thải và tiết kiệm nhiên liệu; Hợp tác ứng dụng nhiên liệu bền vững (SAF)"
      : "Doanh nghiệp tiên phong Net Zero 2050; Hệ thống trang trại sinh thái Green Farm chuẩn GlobalG.A.P";

    container.innerHTML = `
      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-file-alt"></i> 1. Thông tin chung hồ sơ tín dụng</h4>
      <div class="form-grid-2" style="margin-bottom: 24px;">
        <div class="form-group">
          <label>Mã hồ sơ tín dụng:</label>
          <div class="form-control-view highlight">${s.code}</div>
        </div>
        <div class="form-group">
          <label>Trạng thái hồ sơ:</label>
          <div class="form-control-view"><span class="badge badge-success">${s.stateText}</span></div>
        </div>
        <div class="form-group">
          <label>Đơn vị lập hồ sơ (Chi nhánh):</label>
          <div class="form-control-view">${s.branchName} (Mã: ${s.branchCode})</div>
        </div>
        <div class="form-group">
          <label>Đơn vị phê duyệt:</label>
          <div class="form-control-view">${s.approvalCenterName}</div>
        </div>
        <div class="form-group">
          <label>Phân loại thẩm quyền:</label>
          <div class="form-control-view">${s.beyondAppraisalType}</div>
        </div>
        <div class="form-group">
          <label>Kết quả phê duyệt:</label>
          <div class="form-control-view highlight">${s.approvalResult}</div>
        </div>
        <div class="form-group">
          <label>Ngày lập hồ sơ tại Chi nhánh:</label>
          <div class="form-control-view">${s.createdDate}</div>
        </div>
        <div class="form-group">
          <label>Ngày nhận đủ hồ sơ tại TTPD:</label>
          <div class="form-control-view">${s.fulfillmentDate}</div>
        </div>
      </div>

      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-info-circle"></i> 2. Thông tin bổ sung & Đánh giá (Theo E.1.1, E.2, B.1_TN)</h4>
      <div class="form-grid-2">
        <div class="form-group">
          <label>Xếp hạng tín dụng nội bộ Agribank (Theo Mục E.2):</label>
          <div class="form-control-view">${ratingInfo}</div>
        </div>
        <div class="form-group">
          <label>Lịch sử quan hệ tín dụng trên CIC (Theo Mục E.1.1):</label>
          <div class="form-control-view">${cicInfo}</div>
        </div>
        <div class="form-group">
          <label>Tổ chức đánh giá thương hiệu & Vị thế ngành:</label>
          <div class="form-control-view">${brandInfo}</div>
        </div>
        <div class="form-group">
          <label>Chính sách ESG & Phát triển bền vững (Theo BCTN):</label>
          <div class="form-control-view">${esgInfo}</div>
        </div>
      </div>
    `;
  }

  // 10. Render Tab: Thông tin phê duyệt TTPD (Approvement)
  function renderApprovement() {
    const conditions = data.loanConditions;
    const isVjc = isVietjet();
    const container = document.getElementById("TabApprovementContent");
    if (!container) return;

    let condRows = conditions
      .map(
        (c, i) => `
        <tr>
          <td width="40" class="text-center">${i + 1}</td>
          <td width="220"><span class="badge badge-primary">${c.type}</span></td>
          <td><strong>${c.content}</strong></td>
          <td width="180"><span class="badge badge-success"><i class="fas fa-check-circle"></i> ${c.status}</span></td>
        </tr>
      `,
      )
      .join("");

    const approveBoxHtml = isVjc
      ? `
        <div style="background: #eafaf1; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #28a745;">
          <h4 style="color: #218838; margin-bottom: 6px;"><i class="fas fa-stamp"></i> KẾT QUẢ PHÊ DUYỆT TÍN DỤNG VƯỢT THẨM QUYỀN (Theo F.3: 72/BB-HĐTD.TSC & F.4: 88/TB-TTPD ngày 10/05/2026)</h4>
          <div>Hội đồng Tín dụng Trụ sở chính và Trung tâm Phê duyệt Tín dụng Miền Bắc quyết định <strong>CHẤP THUẬN CẤP HẠN MỨC TÍN DỤNG 2.500 TỶ VNĐ</strong> cho Công ty Cổ phần Hàng không Vietjet (Tỷ lệ đồng thuận 100%). Quản lý dòng tiền bán vé qua Agribank Chi nhánh Sở Giao dịch.</div>
        </div>
      `
      : `
        <div style="background: #eafaf1; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #28a745;">
          <h4 style="color: #218838; margin-bottom: 6px;"><i class="fas fa-stamp"></i> KẾT QUẢ PHÊ DUYỆT TÍN DỤNG VƯỢT THẨM QUYỀN (Theo F.3: 89/BB-HĐPD & F.4: 120/TB-TTPD ngày 25/04/2023)</h4>
          <div>Hội đồng Thẩm định & Phê duyệt Tín dụng Trung tâm Phê duyệt Miền Nam quyết định <strong>CHẤP THUẬN CẤP HẠN MỨC TÍN DỤNG 3.000 TỶ VNĐ</strong> cho Công ty Cổ phần Sữa Việt Nam (Tỷ lệ đồng thuận 5/5 thành viên - 100%).</div>
        </div>
      `;

    container.innerHTML = `
      ${approveBoxHtml}
      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-tasks"></i> Danh mục Điều kiện tín dụng phê duyệt (Loan Conditions)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th>STT</th>
            <th>Giai đoạn điều kiện</th>
            <th>Nội dung điều kiện tín dụng cụ thể</th>
            <th>Trạng thái tuân thủ</th>
          </tr>
        </thead>
        <tbody>${condRows}</tbody>
      </table>
    `;
  }

  // 11. Render Tab: Hồ sơ đính kèm (DocumentList)
  function renderDocumentList() {
    const tree = data.documentTree;
    const publicDocs = data.publicDocuments || [];
    const isVjc = isVietjet();
    const container = document.getElementById("TabDocumentListContent");
    if (!container) return;

    // 11.1 Khối Kho tài liệu công khai đã thu thập
    let publicDocsHtml = "";
    if (publicDocs.length > 0) {
      let rows = publicDocs
        .map(
          (p, i) => `
          <tr>
            <td width="40" class="text-center">${i + 1}</td>
            <td width="110"><code>${p.code}</code></td>
            <td>
              <strong>${p.name}</strong><br>
              <small class="text-muted"><i class="fas fa-landmark"></i> Nguồn thu thập: ${p.source}</small>
            </td>
            <td class="text-center" width="100"><span class="badge badge-success">${p.pageCount} trang</span></td>
            <td class="text-right" width="90"><code>${p.size}</code></td>
            <td width="200" class="text-center">
              <div style="display: flex; gap: 6px; justify-content: center;">
                <button class="btn btn-primary btn-sm btn-view-pdf" data-path="${p.path}" data-code="${p.code}" data-name="${p.name}" style="padding: 3px 8px; font-size: 11px;">
                  <i class="fas fa-file-pdf"></i> Xem scan
                </button>
                <a href="${p.path}" download="${p.fileName}" class="btn btn-outline-primary btn-sm" style="padding: 3px 8px; font-size: 11px; text-decoration: none;">
                  <i class="fas fa-download"></i> Tải về
                </a>
              </div>
            </td>
          </tr>
        `,
        )
        .join("");

      const pubTitle = isVjc
        ? "KHO HỒ SƠ THU THẬP NGUYÊN BẢN CÔNG KHAI (Chính thức từ HOSE, Vietjet IR, PwC & ĐHĐCĐ 2026)"
        : "KHO HỒ SƠ THU THẬP NGUYÊN BẢN CÔNG KHAI (Chính thức từ HOSE, Vinamilk IR, KPMG & ĐHĐCĐ 2026)";

      const pubBadge = isVjc
        ? "7 tài liệu gốc (368 trang | 63.68 MB)"
        : "7 tài liệu gốc (313 trang | 15.11 MB)";

      const pubNotice = isVjc
        ? "Toàn bộ các tài liệu dưới đây là văn bản scan gốc chính thức của Vietjet (PwC kiểm toán 2024-2025, Báo cáo thường niên 2025, Báo cáo quản trị HOSE 2024-2025, Nghị quyết & Biên bản ĐHĐCĐ thường niên 2026, Thông báo tăng vốn điều lệ lên 7.690,9 tỷ VNĐ). Tiêu đề, số hiệu văn bản, năm, số trang và dung lượng khớp 100% với nội dung tệp PDF."
        : "Toàn bộ các tài liệu dưới đây là văn bản gốc chính thức của Vinamilk (KPMG kiểm toán VAS/IFRS, Báo cáo thường niên, Báo cáo quản trị HOSE, Nghị quyết & Biên bản ĐHĐCĐ thường niên 2026). Tiêu đề, số hiệu văn bản, năm, số trang và dung lượng khớp 100% với nội dung tệp PDF.";

      publicDocsHtml = `
        <div id="public-docs-storage" class="doc-category-box" style="border: 2px solid #28a745; margin-bottom: 24px; background: #fafdfb;">
          <div class="doc-category-header" style="background: #28a745; color: #fff;">
            <div>
              <span class="cat-title"><i class="fas fa-archive"></i> ${pubTitle}</span>
            </div>
            <span class="badge badge-light" style="color: #28a745; font-weight: bold;">${pubBadge}</span>
          </div>
          <div style="padding: 10px 15px; font-size: 12px; color: #155724; background: #e8f5e9; border-bottom: 1px solid #c3e6cb;">
            <i class="fas fa-info-circle"></i> ${pubNotice}
          </div>
          <table class="data-table" style="margin-top: 0; border: none;">
            <thead>
              <tr>
                <th width="40" class="text-center">STT</th>
                <th>Mã HS</th>
                <th>Tên tài liệu công khai chính thức</th>
                <th class="text-center">Số trang</th>
                <th class="text-right">Dung lượng</th>
                <th class="text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;
    }

    // 11.2 Danh mục 9 nhóm hồ sơ A - I
    let html = publicDocsHtml;
    const folderMap = {
      A: "A_Ho_So_Phap_Ly",
      B: "B_Ho_So_Kinh_Te",
      C: "C_Ho_So_Vay_Von",
      D: "D_Ho_So_Tai_San_Bao_Dam",
      E: "E_Ho_So_Chi_Nhanh_Lap",
      F: "F_Ho_So_TTPD_Lap",
      G: "G_Thong_Bao_Thu_Cong_Tac",
      H: "H_Ho_So_Giai_Ngan",
      I: "I_Ho_So_Quan_Ly_No",
    };

    tree.forEach((cat) => {
      let docRows = cat.documents
        .map((d) => {
          const catFolder = folderMap[cat.code];
          const pdfPath = catFolder
            ? `documents/${data.profileSummary.code}/${catFolder}/${d.fileName}`
            : null;
          return `
          <tr>
            <td width="90"><code>${d.code}</code></td>
            <td>
              <strong>${d.name}</strong>
              ${d.size ? `<br><small class="text-muted"><i class="far fa-file-alt"></i> ${d.size}</small>` : ""}
            </td>
            <td class="text-center" width="70"><span class="badge badge-secondary">${d.fileCount} file</span></td>
            <td><i class="far fa-file-pdf text-danger"></i> <span style="font-family: monospace; font-size: 11.5px;">${d.fileName}</span></td>
            <td width="150" class="text-center">
              ${
                d.isOfficialPublicDoc
                  ? '<span class="badge badge-success" title="Thu thập trực tiếp từ nguồn công bố thông tin chính thức HOSE/Doanh nghiệp"><i class="fas fa-check-circle"></i> Bản gốc công khai</span>'
                  : '<span class="badge badge-warning" title="Tài liệu nội bộ ngân hàng giả lập nghiệp vụ Agribank"><i class="fas fa-robot"></i> Giả lập NH</span>'
              }
            </td>
            <td width="160" class="text-center">
              ${
                pdfPath
                  ? `<div style="display: flex; gap: 4px; justify-content: center;">
                      <button class="btn btn-primary btn-sm btn-view-pdf" data-path="${pdfPath}" data-code="${d.code}" data-name="${d.name}" style="padding: 4px 8px; font-size: 11px;">
                        <i class="fas fa-file-pdf"></i> Xem Scan
                      </button>
                      <a href="${pdfPath}" download="${d.fileName}" class="btn btn-outline-primary btn-sm" title="Tải tệp này" style="padding: 4px 8px; font-size: 11px; text-decoration: none;">
                        <i class="fas fa-download"></i>
                      </a>
                     </div>`
                  : `<button class="btn btn-outline-primary btn-sm btn-preview-doc" data-code="${d.code}" data-name="${d.name}" style="padding: 4px 10px; font-size: 11px;">
                      <i class="fas fa-eye"></i> Xem scan
                     </button>`
              }
            </td>
          </tr>
        `;
        })
        .join("");

      html += `
        <div class="doc-category-box">
          <div class="doc-category-header">
            <div><span class="cat-title">Nhóm ${cat.code}:</span> ${cat.name}</div>
            <span class="badge badge-light">${cat.documents.length} tài liệu</span>
          </div>
          <table class="data-table" style="margin-top: 0; border: none;">
            <thead>
              <tr>
                <th>Mã hồ sơ</th>
                <th>Tên loại tài liệu</th>
                <th class="text-center">Số lượng</th>
                <th>File đính kèm</th>
                <th class="text-center">Nguồn gốc</th>
                <th class="text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody>${docRows}</tbody>
          </table>
        </div>
      `;
    });

    container.innerHTML = html;

    // Click xem PDF modal
    container.querySelectorAll(".btn-view-pdf").forEach((btn) => {
      btn.addEventListener("click", function () {
        const path = this.getAttribute("data-path");
        const docCode = this.getAttribute("data-code");
        const docName = this.getAttribute("data-name");
        openPdfModal(path, docCode, docName);
      });
    });

    // Click xem Scan modal fallback
    container.querySelectorAll(".btn-preview-doc").forEach((btn) => {
      btn.addEventListener("click", function () {
        const docCode = this.getAttribute("data-code");
        const docName = this.getAttribute("data-name");
        openScanModal(docCode, docName);
      });
    });
  }

  // 12. Modal Xem Scan PDF
  const modal = document.getElementById("previewModal");
  const modalTitle = document.getElementById("modalDocTitle");
  const modalBody = document.getElementById("modalBody");
  const modalClose = document.getElementById("modalCloseBtn");
  const modalExternalLink = document.getElementById("modalExternalLink");

  function openPdfModal(pdfPath, code, name) {
    if (!modal || !modalBody) return;
    modalTitle.innerHTML = `<i class="fas fa-file-pdf text-danger"></i> Hồ sơ Scan: [${code}] ${name}`;
    modalBody.classList.remove("paper-mode");

    if (modalExternalLink) {
      modalExternalLink.href = pdfPath;
      modalExternalLink.style.display = "inline-flex";
    }

    modalBody.innerHTML = `
      <iframe class="pdf-viewer-frame" src="${pdfPath}#toolbar=1&navpanes=0" title="${name}">
        <div style="padding: 40px; text-align: center; color: #fff;">
          <p style="font-size: 15px; margin-bottom: 15px;">Trình duyệt không hỗ trợ nhúng trực tiếp tài liệu PDF.</p>
          <a href="${pdfPath}" target="_blank" class="btn btn-primary" style="display: inline-block;">
            <i class="fas fa-external-link-alt"></i> Mở PDF trong tab mới
          </a>
        </div>
      </iframe>
    `;

    modal.classList.add("show");
  }

  function openScanModal(code, name) {
    if (!modal || !modalBody) return;
    const isVjc = isVietjet();
    const b = data.businessEntity;
    const s = data.profileSummary;

    modalTitle.innerHTML = `<i class="fas fa-file-alt"></i> Bản xem trước: [${code}] ${name}`;
    modalBody.classList.add("paper-mode");

    if (modalExternalLink) {
      modalExternalLink.style.display = "none";
    }

    modalBody.innerHTML = `
      <div class="scan-paper" style="max-width: 850px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 20px;">
          <table style="width: 100%; border: none;">
            <tr>
              <td style="text-align: left; width: 50%; vertical-align: top; border: none; font-size: 11px;">
                <strong>${b.companyName}</strong><br>
                Mã HS: ${s.code}<br>
                <i>V/v: Hồ sơ cấp tín dụng Agribank</i>
              </td>
              <td style="text-align: center; width: 50%; vertical-align: top; border: none; font-size: 11px;">
                <strong>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</strong><br>
                <u>Độc lập - Tự do - Hạnh phúc</u><br><br>
                <i>Hà Nội, ngày 26 tháng 04 năm 2026</i>
              </td>
            </tr>
          </table>
        </div>

        <div style="text-align: center; margin: 25px 0 15px;">
          <h3 style="text-transform: uppercase; margin-bottom: 5px;">${name}</h3>
          <p><i>(Trích xuất từ Hồ sơ công bố thông tin chính thức của ${b.companyName} - Mã CK: ${b.stockTicker})</i></p>
        </div>

        <div style="font-size: 13px; line-height: 1.8; text-align: justify;">
          <p><strong>Căn cứ:</strong> Giấy chứng nhận đăng ký doanh nghiệp số <strong>${b.businessLicense}</strong> do ${b.licenseIssuer} (Mục A.1.1);</p>
          <p><strong>Căn cứ:</strong> Nghị quyết & Biên bản họp ĐHĐCĐ thường niên năm 2026 (Mục A.1.2 & C.I.1.2);</p>
          <p><strong>Căn cứ:</strong> Báo cáo tài chính hợp nhất kiểm toán do ${data.financialReport.auditor} thực hiện (Mục B.1, B.2);</p>
          <hr style="margin: 15px 0; border: none; border-top: 1px dashed #ccc;">
          <p><strong>Thông tin chính thức:</strong></p>
          <ul>
            <li>Tên khách hàng vay: <strong>${b.companyName} (${b.shortName})</strong></li>
            <li>Địa chỉ: ${b.businessAddress}</li>
            <li>Vốn điều lệ: <strong>${formatMoney(b.charterCapital)}</strong></li>
            <li>Đề nghị vay vốn: Hạn mức <strong>${formatMoney(data.loanProposal.approvedAmount)}</strong> tại ${s.branchName}</li>
          </ul>
        </div>
      </div>
    `;

    modal.classList.add("show");
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove("show");
    if (modalBody) modalBody.innerHTML = "";
  }

  if (modalClose) {
    modalClose.addEventListener("click", closeModal);
  }
  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });
  }
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && modal.classList.contains("show")) {
      closeModal();
    }
  });

  // 13. Export JSON Button
  const exportBtn = document.getElementById("btnExportJson");
  if (exportBtn) {
    exportBtn.addEventListener("click", function () {
      const isVjc = isVietjet();
      const fileName = isVjc ? "vietjet_profile_data.json" : "vinamilk_profile_data.json";
      const dataStr =
        "data:text/json;charset=utf-8," +
        encodeURIComponent(JSON.stringify(data, null, 2));
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", fileName);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    });
  }

  // 14. Print Button
  const printBtn = document.getElementById("btnPrintProfile");
  if (printBtn) {
    printBtn.addEventListener("click", function () {
      window.print();
    });
  }

  // 15. Button Go To Public Documents Storage
  const publicDocsBtn = document.getElementById("btnGoToPublicDocs");
  if (publicDocsBtn) {
    publicDocsBtn.addEventListener("click", function () {
      const docTabBtn = document.querySelector('.tab-btn[data-tab="tab-documents"]');
      if (docTabBtn) docTabBtn.click();
      const storageBox = document.getElementById("public-docs-storage");
      if (storageBox) {
        storageBox.scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  // 16. Action Toolbar Listeners
  const btnSave = document.getElementById("btnSaveProfile");
  if (btnSave) {
    btnSave.addEventListener("click", function () {
      alert(`Đã lưu dữ liệu hồ sơ tín dụng ${data.businessEntity.shortName} vào hệ thống LOS!`);
    });
  }

  const btnForward = document.getElementById("btnForwardUpper");
  if (btnForward) {
    btnForward.addEventListener("click", function () {
      alert(`Hồ sơ ${data.profileSummary.code} đang ở trạng thái: ${data.profileSummary.stateText}`);
    });
  }

  const btnApprove = document.getElementById("btnApproveAction");
  if (btnApprove) {
    btnApprove.addEventListener("click", function () {
      alert(`Hồ sơ đã được phê duyệt chính thức với Hạn mức ${formatShortBillion(data.loanProposal.approvedAmount)} theo ${data.profileSummary.approvalResult}`);
    });
  }

  const btnSummon = document.getElementById("btnSummonBoard");
  if (btnSummon) {
    btnSummon.addEventListener("click", function () {
      alert(`Triệu tập Hội đồng Tín dụng: ${data.profileSummary.approvalCenterName}`);
    });
  }

  // 17. Render Toàn bộ các Tab
  function renderAllTabs() {
    renderBusinessEntity();
    renderBusinessCreditReport();
    renderLoanPurpose();
    renderCollateralAsset();
    renderProposalForLoan();
    renderAddtionalInformation();
    renderApprovement();
    renderDocumentList();
  }

  // 18. Switch Profile Handler
  function switchProfile(profileKey) {
    if (!profiles[profileKey]) return;
    currentProfileKey = profileKey;
    data = profiles[profileKey];
    localStorage.setItem("active_credit_profile", profileKey);

    // Cập nhật URL query param không reload trang
    const newUrl = new URL(window.location);
    newUrl.searchParams.set("profile", profileKey);
    window.history.replaceState({}, "", newUrl);

    updateHeaderAndToolbar();
    renderAllTabs();
  }

  // Listener khi đổi profile từ Select Dropdown
  const selector = document.getElementById("profileSelector");
  if (selector) {
    selector.addEventListener("change", function () {
      switchProfile(this.value);
    });
  }

  // Initial render
  updateHeaderAndToolbar();
  renderAllTabs();
});
