from darwinmcp.mcp_compat import MCPVersion, detected_mcp_version


def test_version_is_v1_helper():
    assert MCPVersion(1, 25, 0).is_v1 is True
    assert MCPVersion(2, 0, 0).is_v1 is False


def test_detected_returns_mcpversion():
    v = detected_mcp_version()
    assert isinstance(v, MCPVersion)
