# Agent compatibility

Checked: 26 October 2026. The source of truth for execution evidence is the
[validation record](validation.md). Format compatibility alone is not an
end-to-end client test.

| Client | Packaging | Install/discovery guidance | Verification |
|---|---|---|---|
| Codex | Standard `SKILL.md`; no required product-specific metadata | User `~/.codex/skills`; project `.agents/skills` | Local installed skill conventions inspected; executable smoke outcome recorded separately |
| Claude Code | Standard `SKILL.md`; no Claude-only frontmatter | User `~/.claude/skills`; project `.claude/skills` | Official documentation checked; client executable unavailable in authoring environment |
| Cursor | Standard `SKILL.md`; no required custom rules | User `~/.cursor/skills`; project `.cursor/skills` | Official documentation checked; client executable unavailable in authoring environment |

Sources verified on this date:

- [Agent Skills specification](https://agentskills.io/specification): metadata,
  directory structure and progressive resource loading.
- [Claude Code skills](https://code.claude.com/docs/en/skills): local/project
  placement and explicit invocation.
- [Cursor skills](https://cursor.com/docs/skills): placement and discovery.

The installer only copies files. It does not install a model, grant permissions,
configure an MCP server, change agent settings or activate skills inside an
already-running session. Restart/start a fresh session and check the client skill
list. For selective installation, the director's references to specialist names
are optional routing hints; it can continue when a specialist is absent.

Remote/cloud execution needs the installed skill folders inside the workspace
or another location the remote agent actually scans. A GitHub URL alone does
not make every client fetch or activate its skills.

The Godot material describes application-owned adapter contracts. Determine the
game's engine, native plugin and SDK versions and verify their official APIs
before implementation. No claim is made that arbitrary Godot/AdMob plugin
combinations work unchanged.
