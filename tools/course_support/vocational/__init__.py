"""Schedule-driven vocational (TVET) course profile: load, plan, audit.

Kept separate from the Grade 1 audit so that ``course-audit-1.0`` stays unchanged.
"""
CONTRACT = "course-audit-vocational-1.0"
BLOCK_KINDS = ("theory", "practice", "assessment")
PHASE_KINDS = (
    "on_dinh_lop", "dan_nhap", "gioi_thieu_chu_de", "giai_quyet_van_de",
    "kiem_tra", "ket_thuc_van_de", "huong_dan_tu_hoc",
)
VERIFICATION_STATES = ("draft", "teacher_verified", "used_in_class")
