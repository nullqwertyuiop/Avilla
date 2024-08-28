from avilla.core.platform import Abstract, Land, Platform

LAND = Land("qq", [{"name": "Tencent"}], humanized_name="QQ")
PLATFORM = Platform(
    LAND,
    Abstract(
        protocol="lagrange-python",
        maintainers=[{"name": "linwenxuan05"}, {"name": "wyapx"}],
        humanized_name="Lagrange protocol for python",
    ),
    Land(
        "lagrange",
        [{"name": "GraiaProject"}],
        humanized_name="lagrange-python for avilla",
    ),
)
