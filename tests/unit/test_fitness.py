from darwinmcp.eval.fitness_tasks import HelloWorldTask


def test_hello_world_probe_is_python_source():
    t = HelloWorldTask()
    src = t.probe("x = 1")
    assert "compile(" in src
    assert "PASS" in src and "FAIL" in src


def test_hello_world_probe_embeds_variant_safely():
    t = HelloWorldTask()
    # variants containing triple-quotes / quotes must not break the probe string.
    src = t.probe('"""a"""\nx = "y"\n')
    # The probe must compile as a standalone Python module.
    compile(src, "<probe>", "exec")
